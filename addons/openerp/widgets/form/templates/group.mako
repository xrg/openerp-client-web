% if string:
	<table>
		<tr>
			<td>
				<div class="group-expand" style="white-space: nowrap;" onclick="expand_group_option('${expand_grp_id}', event)">
					${string}
				</div>
			</td>
		</tr>
		<tr>	
			<td>
				<div id="${expand_grp_id}" style="display: none; white-space: nowrap;">${display_member(frame)}</div>
			</td>
		</tr>
	</table>
	
% else:
	${display_member(frame)}
% endif
