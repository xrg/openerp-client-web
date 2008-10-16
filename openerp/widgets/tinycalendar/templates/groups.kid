<dl id="calGroups" xmlns:py="http://purl.org/kid/ns#">
    <dt class="calGroupsTitle" py:if="title">${title}</dt>
    <dd>
        <table border="0" class="calGroups" width="100%">
            <input type="hidden" id="_terp_colors" value="${ustr(colors)}"/>
            <tr py:for="x, color in colors.items()">
                <td width="1"><input type="checkbox" class="checkbox" onclick="getCalendar()" checked="${(color[1] in color_values or None) and 'checked'}" value="${color[1]}"/></td>
                <td style="background-color: ${color[-1]}">${color[0]}</td>
            </tr>
        </table>
    </dd>
</dl>
