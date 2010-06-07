<dl id="calGroups">
    % if title:
    <dt class="calGroupsTitle">
        <table>
            <tr>
                <td>
                    ${title}
                </td>
                <td>
                    <a class="button-a" href="javascript: void(0)">${_("Add")}</a>
                </td>
            </tr>
        </table>
    </dt>
    % endif
    <dd>
        <ul class="ul_calGroups">
            <input type="hidden" id="_terp_colors" value="${colors}"/>
            % for x, color in colors.items():
                <li>
                    <input type="checkbox" class="checkbox" onclick="getCalendar()" value="${color[1]}"
                    ${py.checker(color[1] in color_values)}/>
                    <label for="${color[0]}">
                       <a href="javascript: void(0)" style="color: ${color[-1]};">${color[0]}</a>
                    </label>
                </li>
            % endfor
        </ul>
        
    </dd>
</dl>

