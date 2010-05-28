<a ${py.attrs(attrs)} 
	class="button-b" 
	id="${name}" 
	href="javascript: void(0)" 
	onclick="buttonClicked('${name}', '${btype}', '${model}', '${id}', '${confirm}', '${target}');" style="height: 18px;">
	% if string:
		% if icon:
			<div class="button_wid_string" style="background-image: url(${icon});">${string}</div>
		% else:
			<div style="text-align: center;">${string}</div>
		% endif
	%else:
		<img align="center" src="${icon}" width="16" height="16"/>
	% endif
</a>