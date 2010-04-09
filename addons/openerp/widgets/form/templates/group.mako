% if string:
	<div class="group-expand" style="white-space: nowrap;" onclick="expand_group_option('${expand_grp_id}', this)">
		<h2><span>${string}</span></h2>
	</div>
	<table id="groupdata_table">
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
