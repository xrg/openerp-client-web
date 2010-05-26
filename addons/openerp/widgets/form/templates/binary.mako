<div>
    <div id="${name}_binary_add" style="display: none;">
        % if editable and not readonly:
        <input ${py.attrs(attrs)}
            type="file" 
            class="${css_class}" 
            kind="${kind}"
            disabled="disabled" 
            id="${name}" 
            name="${name}"/>
        % endif
    </div>
    <div id="${name}_binary_buttons" class="binary_buttons">
        <span>${value or text or ''}</span>
        % if text:
        <button type="button" onclick="save_binary_data('${name}', '${filename}')">${_("Save As")}</button>
        % endif
        % if editable:
        <button type="button" onclick="add_binary('${name}')">${_("Change")}</button>
        % endif
    </div>
    % if editable and error:
    <span class="fielderror">${error}</span>
    % endif
</div>

