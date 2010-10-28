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
        this.view_tree = jQuery("#view_tree")[0];
        this.trees = {};
        this.current = treeGrids['tree_' + current];

        var tree = this;
        jQuery('#treeview-tree-selector').change(function () {
            var $this = jQuery(this).find('option:selected');
            tree.openTree(
                parseInt($this.val(), 10),
                jQuery.parseJSON($this.attr('data-ids'))
            );
        });

        this.trees[this.current.id] = this.current;
    },

    openTree: function(id, ids) {
        if (openobject.http.AJAX_COUNT > 0) {
            return;
        }
        ids = ids == ''? 'None' : ids;

        var tree = this.trees['tree_' + id] || null;
        if (!tree) {
            var $span = jQuery('<span>', {'id': 'tree_' + id})
                            .appendTo(this.view_tree);
            tree = this.current.copy($span[0], null, ids);
            this.trees[tree.id] = tree;

            tree.render();
        }

        jQuery(idSelector(this.current.id)).hide();

        this.current = tree;
        if (tree.table) {
            jQuery(tree.table).show();
        }
    },

    repr: function() {
        return "[TreeView]";
    },
    
    toString: MochiKit.Base.forwardCall("repr")
    
};
