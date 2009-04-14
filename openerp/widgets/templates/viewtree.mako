<form method="post" id="${name}" name="${name}" action="${action}">
    <input type="hidden" id="_terp_model" name="_terp_model" value="${model}"/>
    <input type="hidden" id="_terp_domain" name="_terp_domain" value="${str(domain)}"/>
    <input type="hidden" id="_terp_context" name="_terp_context" value="${str(context)}"/>
    <input type="hidden" id="_terp_view_id" name="_terp_view_id" value="${str(view_id)}"/>
    
    % for field in hidden_fields:
        ${display_child(field)}
    % endfor
    
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
% if tree:
    ${tree.display()}
% endif
</form>

