<form id="view_form" name="view_form" action="">
    <input type="hidden" name="view_id" id="view_id" value="${view_id}"/>
    <input type="hidden" name="xpath_expr" id="xpath_expr" value="${xpath_expr}"/>
    <table width="100%">
        <tr>
            <td class="label" width="5"><label for="node">${_("Node Type:")}</label></td>
            <td class="item" width="100">
                <select id="node" name="node" onchange="toggleFields(this)">
                    % for node in nodes:
                    <option value="${node}" ${py.selector(node=='field')}>${node}</option>
                    % endfor
                </select>
            </td>
            <td class="item">
                <select id="name" name="name" style="display: ${('field' in nodes or 'none') or None}">
                    <option value=""></option>
                    % for field in fields:
                    <option value="${field}">${field}</option>
                    % endfor
                </select>
            </td>
            <td width="5" nowrap="nowrap">
                <a id="new_field" name="new_field" class="button" href="javascript: void(0)" onclick="onNew('${model}', window)">${_("New Field")}</a>
            </td>
        </tr>
        <tr>
            <td class="label" width="5"><label for="position">${_("Position:")}</label></td>
            <td class="item" width="100">
                <select id="position" name="position">
                    % for v,p in positions:
                    <option value="${v}">${p}</option>
                    % endfor
                </select>
            </td>
            <td></td>
            <td></td>
        </tr>
    </table>
</form>
