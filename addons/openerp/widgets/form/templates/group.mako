% if string:
	<table>
		<tr>
			<td>
				% if default:
					<div class="group-collapse" style="white-space: nowrap;" onclick="expand_group_option('${expand_grp_id}', event)">
						${string}
					</div>
				%else:
					<div class="group-expand" style="white-space: nowrap;" onclick="expand_group_option('${expand_grp_id}', event)">
						${string}
					</div>
				% endif
			</td>
		</tr>
		<tr>	
			<td>
				% if default:
					<div id="${expand_grp_id}" style="white-space: nowrap;">${display_member(frame)}</div>
				% else:
					<div id="${expand_grp_id}" style="display: none; white-space: nowrap;">${display_member(frame)}</div>
				% endif
			</td>
		</tr>
	</table>
	
% else:
	${display_member(frame)}
% endif
