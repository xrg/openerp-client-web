% if string:
	<table>
		<tr>
			<td>
				<div class="group-expand" style="white-space: nowrap;" onclick="if(this.className=='group-expand') {this.className='group-collapse';getElement('group_records').style.display='';} else{this.className='group-expand';getElement('group_records').style.display='none';}">
					<div>${string}</div>
				</div>
			</td>
		</tr>
		<tr>	
			<td>
				<div id="group_records" style="display: none; white-space: nowrap;">${display_member(frame)}</div>
			</td>
		</tr>
	</table>
	
% else:
	${display_member(frame)}
% endif
