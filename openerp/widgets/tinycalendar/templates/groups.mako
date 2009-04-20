<dl id="calGroups">
    % if title:
    <dt class="calGroupsTitle">${title}</dt>
    % endif
    <dd>
        <table border="0" class="calGroups">
            <input type="hidden" id="_terp_colors" value="${colors}"/>
            % for x, color in colors.items():
            <tr>
                <td width="1"><input type="checkbox" class="checkbox" onclick="getCalendar()" checked="${(color[1] in color_values or None) and 'checked'}" value="${color[1]}"/></td>
                <td style="background-color: ${color[-1]}">${color[0]}</td>
            </tr>
            % endfor
        </table>
    </dd>
</dl>

