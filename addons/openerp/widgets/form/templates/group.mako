% if string:
	<table>
		<tr>
			<td>
				% if default:
					<div id="group_${expand_grp_id}" class="group-collapse" style="white-space: nowrap;">
						${string}
					</div>
				%else:
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
			<script type="text/javascript">
				var view_type = jQuery('[id*= _terp_view_type]').val();
				if(view_type == 'form') {
					jQuery('div[id=group_${expand_grp_id}]').toggleClass('group-collapse');
					jQuery('[id=${expand_grp_id}]').css('display', 'block');
				}
				
				else {
					jQuery('div[id=group_${expand_grp_id}]').click(function() {
					var action;
					jQuery(this).toggleClass(function(index, class) {
						if(class == 'group-expand') {
							jQuery('[id=${expand_grp_id}]').css('display', 'block');
							jQuery(this).removeClass(class);
							action = 'expand';
							return 'group-collapse';
					}
					else  {
						jQuery('[id=${expand_grp_id}]').css('display', 'none');
						jQuery(this).removeClass(class);
						action = 'collapse';
						return 'group-expand';
					}
					});
					MochiKit.Signal.signal(jQuery('[id=search_filter_data]'), 'groupby-toggle', action);
					});
				}
				</script>
		</tr>
	</table>
	
% else:
	${display_member(frame)}
% endif
