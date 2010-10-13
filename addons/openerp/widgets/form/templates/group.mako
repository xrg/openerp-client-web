% if string:
	% if view_type == 'form':
		<fieldset>
			<legend>${string}</legend>
			${display_member(frame)}
		</fieldset>
	% else:
		% if default:
			<div id="group_${expand_grp_id}" onclick="collapse_expand(this, '#${expand_grp_id}', '#groupdata_table');" class="group-collapse">
				<h2>${string}</h2>
			</div>
		% else:
			<div id="group_${expand_grp_id}" onclick="collapse_expand(this, '#${expand_grp_id}', '#groupdata_table');" class="group-expand">
				<h2>${string}</h2>
			</div>
		% endif

		<table id="groupdata_table">
			<tr>
				<td>
					% if default:
						<div id="${expand_grp_id}" class="group-data">${display_member(frame)}</div>
					% else:
						<div id="${expand_grp_id}" class="group-data" style="display: none;">${display_member(frame)}</div>
					% endif
				</td>
			</tr>
		</table>
	% endif
% else:
	${display_member(frame)}
% endif
