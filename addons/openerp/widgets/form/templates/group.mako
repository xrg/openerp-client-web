% if string:
	% if view_type == 'form':
		<fieldset>
			<legend>${string}</legend>
			${display_member(frame)}
		</fieldset>
	% else:
		% if default:
			<div id="group_${expand_grp_id}" class="group-collapse" style="white-space: nowrap;">
				<h2><span>${string}</span></h2>
			</div>
		% else:
			<div id="group_${expand_grp_id}" class="group-expand" style="white-space: nowrap;">
				<h2><span>${string}</span></h2>
			</div>
		% endif
		
		<table id="groupdata_table" style="display: block;">
			<tr>	
				<td>
					% if default:
						<div id="${expand_grp_id}" class="group-data" style="white-space: nowrap;">${display_member(frame)}</div>
					% else:
						<div id="${expand_grp_id}" class="group-data" style="display: none; white-space: nowrap;">${display_member(frame)}</div>
					% endif
				</td>
			</tr>
		</table>
		<script type="text/javascript">
			jQuery('#group_${expand_grp_id}').click(function() {
				jQuery(this).toggleClass('group-collapse', 100);
				jQuery('#${expand_grp_id}').toggle("slow");
				jQuery('#groupdata_table').css('display', 'block');
			});
		</script>
	% endif
% else:
	${display_member(frame)}
% endif
