% if string:
	% if view_type == 'form':
		<fieldset>
			<legend>${string}</legend>
			${display_member(frame)}
		</fieldset>
	% else:
		<table>
			<tr>
				<td>
					% if default:
						<div id="group_${expand_grp_id}" class="group-collapse" style="white-space: nowrap;">
							${string}
						</div>
					% else:
						<div id="group_${expand_grp_id}" class="group-expand" style="white-space: nowrap;">
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
		<script type="text/javascript">
			jQuery('div[id=group_${expand_grp_id}]').click(function() {
				var action;
				jQuery(this).toggleClass(function (index, cls) {
					if(cls == 'group-expand') {
						jQuery('[id=${expand_grp_id}]').css('display', 'block');
						jQuery(this).removeClass(cls);
						action = 'expand';
						return 'group-collapse';
					} else {
						jQuery('[id=${expand_grp_id}]').css('display', 'none');
						jQuery(this).removeClass(cls);
						action = 'collapse';
						return 'group-expand';
					}
				});
				MochiKit.Signal.signal(jQuery('[id=search_filter_data]'), 'groupby-toggle', action);
			});
		</script>
	% endif
% else:
	${display_member(frame)}
% endif
