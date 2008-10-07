<form xmlns:py="http://purl.org/kid/ns#" id="view_form" name="view_form" onsubmit="return false" action="">
    <input type="hidden" name="view_id" id="view_id" value="${view_id}"/>
    <input type="hidden" name="xpath_expr" id="xpath_expr" value="${xpath_expr}"/>
    <table width="100%">
        <tr>
            <td class="label" width="5">Node Type:</td>
            <td class="item" width="100">
                <select id="node" name="node" onchange="toggleFields(this)">
                    <option py:for="node in nodes" value="${node}" selected="${tg.selector(node=='field')}">${node}</option>
                </select>
            </td>
            <td class="item">
                <select id="name" name="name" style="display: ${('field' in nodes or 'none') or None}">
                    <option value=""></option>
                    <option py:for="field in fields" value="${field}">${field}</option>
                </select>
            </td>
            <td width="5" nowrap="nowrap">
                <button id="new_field" name="new_field" class="button" onclick="onNew('$model')">New Field</button>
            </td>
        </tr>
        <tr>
            <td class="label" width="5">Position:</td>
            <td class="item" width="100">
                <select id="position" name="position">
                    <option py:for="v,p in positions" value="$v">$p</option>
                </select>
            </td>
            <td></td>
            <td></td>
        </tr>
    </table>
</form>
