<div class="dashbar" id="${name}">
    % for dashlet in children:
	    % if not getattr(dashlet, 'btype', False):
		    <div class="dashlet" id="dashlet_${dashlet.name}">
                <!--<ul class="side">
                    <li><a class="move" href="./">Move</a></li>
                </ul>-->
                <h2 class="dashlet-drag">
                    <a href="#" class="dashlet-title" onclick="submit_form('dashlet', '${dashlet.name}')">${dashlet.string}</a>
                    <a href="#" class="move">Move</a>
                </h2>
		        <div class="dashlet-content">${display_member(dashlet)}</div>
		    </div>
	    % else:
	        ${display_member(dashlet)}
	    % endif 
    % endfor
</div>

