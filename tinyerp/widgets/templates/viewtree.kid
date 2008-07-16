<form xmlns:py="http://purl.org/kid/ns#" method="post" id="${name}" name="${name}" action="${action}">
    <input type="hidden" id="_terp_model" name="_terp_model" value="${model}"/>
    <input type="hidden" id="_terp_domain" name="_terp_domain" value="${str(domain)}"/>
    <input type="hidden" id="_terp_context" name="_terp_context" value="${str(context)}"/>
    
    <span py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
    <script type="text/javascript">
    
        function onSelection(evt, node) {
        
            var selection = node.tree.selection;
            
            var values = MochiKit.Base.map(function(n){
                return n.record.id;
            }, selection);
            
            MochiKit.DOM.getElement('tree_ids').value = values;
        }
        
        function onHeaderClick(evt, header) {
            tree.ajax_params.sort_by = header.name;
            tree.ajax_params.sort_order = tree.ajax_params.sort_order == "dsc" ? "asc" : "dsc";
            tree.reload();
        }
        
    </script>
    <input type="hidden" id="tree_ids" name="ids"/>
    <span py:if="tree" py:replace="tree.display(value_for(tree), **params_for(tree))"/>
</form>