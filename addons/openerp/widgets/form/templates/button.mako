<a class="button-b"
   id="${name}"
   href="javascript: void(0)"
   onclick="buttonClicked('${name}', '${btype}', '${model}', '${id}', '${confirm}', '${target}', getNodeAttribute(this, 'context'));"
   style="height: 18px; text-align: center;"
   ${py.attrs(attrs, context=ctx)}>
        % if string:
			% if icon:
				<img style="vertical-align: middle; padding:1px;" src="${icon}" width="16" height="16" alt=""></img>&nbsp;<span style="vertical-align: middle;">${string}</span>
			% else:
				<div style="text-align: center; padding-top: 3px;">${string}</div>
			% endif
		%else:
			<img align="middle" src="${icon}" width="16" height="16" alt=""></img>
		% endif
</a>
% if default_focus:
    <script type="text/javascript">
       jQuery('#${name}').focus();
       jQuery('#${name}').keypress(function(evt) {
            if(evt.keyCode == 0) {
                jQuery(this).click();
            }
            if(evt.keyCode == 27) {
                window.close();
            }
       });
    </script>
% endif

