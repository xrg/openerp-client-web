<form id="view_form" name="view_form" action="">
    <input type="hidden" name="view_id" id="view_id" value="${view_id}"/>
    <input type="hidden" name="xpath_expr" id="xpath_expr" value="${xpath_expr}"/>
    <table>
        % for ed in editors:
        <tr>
            <td class="label">${ed.label}:</td>
            <td class="item" width="100%">${ed.display()}</td>
        </tr>
        % endfor
    </table>
</form>
