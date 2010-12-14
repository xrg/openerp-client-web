<button class="button-b"
        id="${name}"
        name="${name}"
        type="button"
        href="javascript: void(0)"
        % if editable:
        onclick="buttonClicked('${name}', '${btype}', '${model}', '${id}', '${confirm}', '${target}', getNodeAttribute(this, 'context'));"
        % endif
        style="height: 20px;"
        ${py.attrs(attrs, context=ctx)}>
    % if string:
        % if icon:
            <img src="${icon}" width="16" height="16" alt="">&nbsp;<span>${string}</span>
        % else:
            <div style="text-align: center; padding-top: 3px;">${string}</div>
        % endif
    %else:
        <img align="middle" src="${icon}" width="16" height="16" alt="">
    % endif
</button>

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

