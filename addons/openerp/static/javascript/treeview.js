var TreeView = function(current) {

    var cls = arguments.callee;
    if (!(this instanceof cls)) {
        return new cls(current);
    }
  
    this.__init__(current);
};

TreeView.prototype = {

    __class__: TreeView,
    
    __init__: function(current) {
        
        this.view_tree = openobject.dom.get("view_tree");
                
        this.trees = {};
        this.current = window['tree_' + current];
        this.current_button = openobject.dom.select("tr.selected", "treeview")[0];
                
        this.trees[this.current.id] = this.current;
    },
        
    openTree: function(id, ids, elem) {
    
        if (openobject.http.AJAX_COUNT > 0) {
            return;
        }
        ids = ids == ''? 'None' : ids;
    	
        var tree = this.trees['tree_' + id] || null;
        
        MochiKit.DOM.removeElementClass(this.current_button, "selected");
        MochiKit.DOM.hideElement(this.current.id);
        
        if (!tree) {
            
            var span = MochiKit.DOM.SPAN({'id': 'tree_' + id});
            this.view_tree.appendChild(span);
            
            tree = this.current.copy(span, null, ids);
            this.trees[tree.id] = tree;
            
            tree.render();
        }
        
        this.current = tree;
        this.current_button = elem;
        
        MochiKit.DOM.addElementClass(this.current_button, "selected");
        
        if (tree.table) {
            tree.table.style.display = "";
        }
    },
    
    switchItem: function() {

        var selection = openobject.dom.get('_terp_ids').value;
        
        if (!selection) {
            return alert(_('You must select at least one record.'));
        }
        
        var form = document.forms['view_tree'];
        var args = {
            '_terp_selection': '[' + selection + ']'
        };

        setNodeAttribute(form, 'action', openobject.http.getURL('/openerp/tree/switch', args));
        form.method = 'post';
        form.submit();
    
    },
    
    repr: function() {
        return "[TreeView]";
    },
    
    toString: MochiKit.Base.forwardCall("repr")
    
};
