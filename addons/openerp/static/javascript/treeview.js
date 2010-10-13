var treeGrids;
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
        this.current_button = jQuery('#treeview tr.selected').get(0);

        this.trees[this.current.id] = this.current;
    },

    openTree: function(id, ids, elem) {
        if (openobject.http.AJAX_COUNT > 0) {
            return;
        }
        ids = ids == ''? 'None' : ids;

        var tree = this.trees['tree_' + id] || null;

        jQuery(this.current_button).removeClass("selected");
        jQuery('#'+this.current.id).hide();

        if (!tree) {
            var span = jQuery('<span>', {'id': 'tree_' + id});
            jQuery(this.view_tree).append(span);
            tree = this.current.copy(span[0], null, ids);
            this.trees[tree.id] = tree;

            tree.render();
        }

        this.current = tree;
        this.current_button = elem;

        jQuery(this.current_button).addClass('selected');

        if (tree.table) {
            jQuery(tree.table).show();
        }
    },

    switchItem: function() {
        var selection = jQuery('#_terp_ids').val();
        if (!selection) {
            return error_display(_('You must select at least one record.'));
        }

        jQuery('#view_tree').attr({
            'action': openobject.http.getURL('/openerp/tree/switch', {
                '_terp_selection': '[' + selection + ']'
            }),
            'method': 'post'
        }).submit();
    },

    repr: function() {
        return "[TreeView]";
    },
    
    toString: MochiKit.Base.forwardCall("repr")
    
};
