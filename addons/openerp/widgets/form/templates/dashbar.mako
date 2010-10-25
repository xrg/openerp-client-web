<div class="dashbar" id="${name}">
    % for dashlet in children:
	    % if not getattr(dashlet, 'btype', False):
		    <div class="dashlet" id="dashlet_${dashlet.name}">
		        <div class="dashlet-title">
		            <table>
		                <tr>
		                    <td style="padding: 0 5px 0 5px;">${dashlet.string}</td>
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
	    % else:
	        ${display_member(dashlet)}
	    % endif 
    % endfor
</div>

