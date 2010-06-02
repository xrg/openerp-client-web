<a ${py.attrs(attrs, context=ctx)} 
	class="button-b" 
	id="${name}" 
	href="javascript: void(0)" 
	onclick="buttonClicked('${name}', '${btype}', '${model}', '${id}', '${confirm}', '${target}', getNodeAttribute(this, 'context'));" style="height: 18px;">
	% if string:
		% if icon:
			<div style="text-align: center; background-image: url(${icon});background-repeat: no-repeat; padding: 3px 0 0 20px; height: 17px;">${string}</div>
		% else:
			<div style="text-align: center;">${string}</div>
		% endif
	%else:
		<img align="center" src="${icon}" width="16" height="16"/>
	% endif
</a>