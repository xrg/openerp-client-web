<div class="dashbar" id="${name}">
    % for dashlet in children:
    <div class="dashlet" id="dashlet_${dashlet.name}">
        <div class="dashlet-title">
            <table>
                <tr>
                    <td width="100%">${dashlet.string}</td>
                    <td>
                        <img class="dashlet-button" 
                             src="/openerp/static/images/stock/gtk-zoom-in.png" 
                             onclick="submit_form('dashlet', '${dashlet.name}', 'new')"/>
                    </td>
                </tr>
            </table>
        </div>
        <div class="dashlet-content">${display_member(dashlet)}</div>
    </div>
    % endfor
</div>

