<table xmlns:py="http://purl.org/kid/ns#" width="100%" height="100%">
    <tr>
        <td class="toolbar">Add New Node</td>
    </tr>
    <tr>
        <td height="100%" valign="top">
            <form id="view_form" name="view_form" onsubmit="return false" action="">
                <input type="hidden" name="view_id" id="view_id" value="${view_id}"/>
                <input type="hidden" name="xpath_expr" id="xpath_expr" value="${xpath_expr}"/>
                <table>
                    <tr>
                        <td class="label">Node Type:</td>
                        <td class="item" width="100">
                            <select id="node" name="node" onchange="getElement('name').style.display = this.value == 'field' ? '' : 'none'">
                                <option py:for="node in nodes" value="${node}" selected="${tg.selector(node=='field')}">${node}</option>
                            </select>
                        </td>
                        <td class="item">
                            <select id="name" name="name">
                                <option value=""></option>
                                <option py:for="field in fields" value="${field}">${field}</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td class="label">Position:</td>
                        <td class="item">
                            <select id="type" name="position">
                                <option value="after">after</option>
                                <option value="before">before</option>
                            </select>
                        </td>
                        <td class="item">
                        </td>
                    </tr>
                </table>
            </form>
        </td>
    </tr>
    <tr>
        <td>
            <div class="toolbar"><button class="button" onclick="doAdd()">Update</button></div>
        </td>
    </tr>
</table>