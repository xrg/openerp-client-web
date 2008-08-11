<div xmlns:py="http://purl.org/kid/ns#" class="dashbar">
    <div class="dashlet" id="dashlet_${dashlet.name}" py:for="dashlet in children">
        <div class="dashlet-title">
            <table>
                <tr>
                    <td width="100%" py:content="dashlet.string"></td>
                    <td>
                        <img class="dashlet-button" 
                             src="/static/images/stock/gtk-zoom-in.png" 
                             onclick="submit_form('dashlet', '${dashlet.name}', null, 'new')"/>
                    </td>
                </tr>
            </table>
        </div>
        <div class="dashlet-content" py:content="dashlet.display(value_for(dashlet), **params_for(dashlet))"/>
    </div>
</div>
