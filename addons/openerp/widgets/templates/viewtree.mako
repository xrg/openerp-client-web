<form method="post" id="${name}" name="${name}" action="${action}">
    <input type="hidden" id="_terp_id" name="_terp_id"/>
    <input type="hidden" id="_terp_ids" name="_terp_ids"/>
    <input type="hidden" id="_terp_model" name="_terp_model" value="${model}"/>
    <input type="hidden" id="_terp_domain" name="_terp_domain" value="${domain}"/>
    <input type="hidden" id="_terp_context" name="_terp_context" value="${ctx}"/>
    <input type="hidden" id="_terp_view_id" name="_terp_view_id" value="${view_id}"/>
    
    % for field in hidden_fields:
        ${display_member(field)}
    % endfor
    
    <script type="text/javascript">
        function onSelection(evt, node) {
        
            var selection = node.tree.selection;
            
            var values = MochiKit.Base.map(function(n){
                return n.record.id;
            }, selection);
            
            openobject.dom.get('_terp_id').value = values.length ? values[0] : '';
            openobject.dom.get('_terp_ids').value = values;
        }
    </script>
    
% if tree:
    ${tree.display()}
% endif

</form>

