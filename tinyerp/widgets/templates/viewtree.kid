<form xmlns:py="http://purl.org/kid/ns#" method="post" id="${name}" name="${name}" action="${action}">
    <input type="hidden" name="_terp_model" value="${model}"/>
    <input type="hidden" name="_terp_domain" value="${str(domain)}"/>
    <input type="hidden" name="_terp_context" value="${str(context)}"/>

    <span py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
    <script type="text/javascript">
        function onselection(rows){
            var values = map(function(row){
                return row.id.split('_').pop();
            }, rows);

            $('tree_ids').value = values;
        }
    </script>

    <input type="hidden" id="tree_ids" name="ids"/>
    <span py:if="tree" py:replace="tree.display(value_for(tree), **params_for(tree))"/>
</form>