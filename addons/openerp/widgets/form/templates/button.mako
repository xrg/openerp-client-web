<a class="button-b"
   id="${name}"
   href="javascript: void(0)"
   onclick="buttonClicked('${name}', '${btype}', '${model}', '${id}', '${confirm}', '${target}', getNodeAttribute(this, 'context'));"
   style="height: 18px;"
   ${py.attrs(attrs, context=ctx)}>
        % if string:
			% if icon:
				<div class="button_wid_string" style="background-image: url(${icon}); padding-top: 3px;">${string}</div>
			% else:
				<div style="text-align: center; padding-top: 3px;">${string}</div>
			% endif
		%else:
			<img align="middle" src="${icon}" width="16" height="16" alt="">
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

