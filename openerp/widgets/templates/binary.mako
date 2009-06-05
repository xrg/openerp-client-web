<div>
    <div id="${name}_binary_add" style="display: none;">
        % if editable and not readonly and not filename:
        <input ${py.attrs(attrs)}
            type="file" 
            class="${css_class}"
            kind="${kind}"
            disabled="disabled" 
            id="${name}"
            name="${name}"/>
        % endif
        % if editable and filename and not readonly:
        <input ${py.attrs(attrs)}
            type="file" 
            class="${css_class}" 
            kind="${kind}"
            disabled="disabled" 
            id="${name}" 
            name="${name}"/>
        % endif
    </div>
    <div id="${name}_binary_buttons" style="white-space: nowrap; width: 150px;">
        <span id='${name}_text_'>${value or text or ''}</span>
        % if editable and not text:
        <button type="button" onclick="add_binary('${name}')">${_("Add")}</button>
        % endif
        % if text:
        <button type="button" onclick="save_binary_data('${name}', '${filename}')">${_("Save As")}</button>
        % endif
        % if text and not readonly and editable:
        <button type="button" 
            onclick="clear_binary_data('${name}', '${filename}')">${_("Clear")}</button>
        % endif
    </div>
    % if editable and error:
    <span class="fielderror">${error}</span>
    % endif
</div>

