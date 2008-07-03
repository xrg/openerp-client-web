<table xmlns:py="http://purl.org/kid/ns#" width="100%" height="100%">
    <tr>
        <td class="toolbar">Add New Node</td>
    </tr>
    <tr>
        <td height="100%" valign="top">
            <form id="view_form" name="view_form" onsubmit="return false" action="">
                <input type="hidden" name="view_id" id="view_id" value="${view_id}"/>
                <input type="hidden" name="rec_id" id="rec_id" value="${rec_id}"/>
                <input type="hidden" name="rec_model" id="rec_model" value="${rec_model}"/>
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
        </td>
    </tr>
    <tr>
        <td>
            <div class="toolbar">
                <button class="button" onclick="doAdd()">Update</button>
                <button class="button" onclick="getElement('view_ed').innerHTML=''">Cancel</button>
            </div>
        </td>
    </tr>
</table>