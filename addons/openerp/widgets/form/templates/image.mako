% if editable and not readonly:
    <div id="${name}_binary_add" style="display: none;">
        <input type="file" disabled="disabled" id="${name}" name="${name}"/>
    </div>
    <div id="${name}_binary_buttons" class="binary_buttons">
        <a class="button-a" href="javascript: void(0)" onclick="add_binary('${name}')">${_("Replace image")}</a>
        <br/>
        <img
            id="${field}_img"
            name="${name}"
            border='1'
            alt=""
            align="left"
            src="${src}"
            % if width:
                width="${width}"
            % endif
            % if height:
                height="${height}"
            % endif
            ${py.attrs(attrs)}
        />
    </div>
% else:
    <div align="center">
        <img
            id="${field}"
            name="${name}"
            border='1'
            src="${src}"
            % if width:
                width="${width}"
            % endif
            % if height:
                height="${height}"
            % endif
        />
    </div>
% endif

