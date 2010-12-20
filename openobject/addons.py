import os
import imp
import itertools

import cherrypy
import openobject.tools.ast
from openobject import errors, paths


class Graph(dict):

    def addNode(self, name, deps):
        max_depth, father = 0, None
        for n in [Node(x, self) for x in deps]:
            if n.depth >= max_depth:
                father = n
                max_depth = n.depth
        if father:
            father.addChild(name)
        else:
            Node(name, self)

    def __iter__(self):
        level = 0
        done = set(self.keys())
        while done:
            level_modules = [(name, module) for name, module in self.items() if module.depth==level]
            for name, module in level_modules:
                done.remove(name)
                yield module
            level += 1


class Singleton(object):
    def __new__(cls, name, graph):
        if name in graph:
            inst = graph[name]
        else:
            inst = object.__new__(cls)
            inst.name = name
            graph[name] = inst
        return inst


class Node(Singleton):

    def __init__(self, name, graph):
        self.name = name
        self.graph = graph
        if not hasattr(self, 'children'):
            self.children = []
        if not hasattr(self, 'depth'):
            self.depth = 0

    def addChild(self, name):
        node = Node(name, self.graph)
        node.depth = self.depth + 1
        if node not in self.children:
            self.children.append(node)
        for attr in ('init', 'update', 'demo'):
            if hasattr(self, attr):
                setattr(node, attr, True)
        self.children.sort(lambda x, y: cmp(x.name, y.name))

    def __setattr__(self, name, value):
        super(Singleton, self).__setattr__(name, value)
        if name in ('init', 'update', 'demo'):
            import openobject.tools._utils as tools
            tools.config[name][self.name] = 1
            for child in self.children:
                setattr(child, name, value)
        if name == 'depth':
            for child in self.children:
                setattr(child, name, value + 1)

    def __iter__(self):
        return itertools.chain(iter(self.children), *map(iter, self.children))

    def __str__(self):
        return self._pprint()

    def _pprint(self, depth=0):
        s = '%s\n' % self.name
        for c in self.children:
            s += '%s`-> %s' % ('   ' * depth, c._pprint(depth+1))
        return s

def exists(module):
    return os.path.exists(paths.addons(module, '__openerp__.py'))

def get_info(module):
    mod_path = paths.addons(module)
    if not os.path.isdir(mod_path):
        return {}

    terp_file = os.path.join(mod_path, '__openerp__.py')
    if not os.path.isfile(terp_file):
        return {}

    try:
        return openobject.tools.ast.literal_eval(open(terp_file).read())
    except:
        cherrypy.log('module %s: eval file %s' % (module, terp_file), "ERROR")
        raise

def create_graph(module_list):
    graph = Graph()
    upgrade_graph(graph, module_list)
    return graph

def upgrade_graph(graph, module_list):

    packages = []
    len_graph = len(graph)

    for module in module_list:
        info = get_info(module)
        if info.get('installable', True):
            packages.append((module, info.get('depends', []), info))

    dependencies = dict([(p, deps) for p, deps, _ in packages])
    current, later = set([p for p, _, _ in packages]), set()

    while packages and current > later:
        package, deps, data = packages[0]

        # if all dependencies of 'package' are already in the graph, add 'package' in the graph
        if reduce(lambda x, y: x and y in graph, deps, True):
            if not package in current:
                packages.pop(0)
                continue
            later.clear()
            current.remove(package)
            graph.addNode(package, deps)
            node = Node(package, graph)
            node.data = data
        else:
            later.add(package)
            packages.append((package, deps, data))
        packages.pop(0)

    for package in later:
        unmet_deps = filter(lambda p: p not in graph, dependencies[package])
        cherrypy.log('module %s: Unmet dependencies: %s' % (package, ', '.join(unmet_deps)), "ERROR")

    result = len(graph) - len_graph
    if result != len(module_list):
        cherrypy.log('Not all modules have loaded.', "ERROR")

    return result


def imp_module(name):
    fp, pathname, description = imp.find_module(name, [paths.addons()])
    try:
        return imp.load_module(name, fp, pathname, description)
    finally:
        if fp:
            fp.close()


from openobject import i18n
from openobject import pooler

def load_module_graph(db_name, graph, config):

    pool = pooler.get_pool()

    for package in graph:

        if package.name in _loaded_addons:
            continue

        cherrypy.log("Loading module '%s'" % package.name, "INFO")

        imp_module(package.name)

        static = paths.addons(package.name, 'static')
        if os.path.isdir(static):
            from openobject.widgets import register_resource_directory
            register_resource_directory(config, package.name, static)

        addon_path = paths.addons(package.name)
        if os.path.isdir(paths.addons(package.name, 'po')):
            i18n.load_translations(addon_path)
            i18n.load_translations(addon_path, domain="javascript")

        _loaded_addons[package.name] = True

    for package in graph:
        pool.load(package.name)


_loaded = {}
_loaded_addons = {}

def get_local_addons():
    return [f for f in os.listdir(paths.addons()) \
              if os.path.isfile(paths.addons(f, "__openerp__.py"))]

def load_addons(db_name, config):
    if db_name in _loaded:
        return

    base_addons = [m for m in get_local_addons() if get_info(m).get("active")]

    graph = create_graph(base_addons)
    load_module_graph(db_name, graph, config)

    try:
        obj = pooler.get_pool().get_controller("/openerp/modules")
        new_modules = obj.get_new_modules()
    except errors.AuthenticationError:
        new_modules = []

    new_modules_in_graph = upgrade_graph(graph, new_modules)
    if new_modules_in_graph:
        load_module_graph(db_name, graph, config)

    _loaded[db_name] = True
