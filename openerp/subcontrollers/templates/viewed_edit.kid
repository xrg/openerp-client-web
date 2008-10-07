<form xmlns:py="http://purl.org/kid/ns#" id="view_form" name="view_form" onsubmit="return false" action="">
    <input type="hidden" name="view_id" id="view_id" value="${view_id}"/>
    <input type="hidden" name="xpath_expr" id="xpath_expr" value="${xpath_expr}"/>
    <table>
        <tr py:for="ed in editors">
            <td class="label">${ed.label}:</td>
            <td class="item" width="100%" py:content="ed.display()"></td>
        </tr>
    </table>
</form>
