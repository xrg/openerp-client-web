<div>
    % if bin_data and not value_bin_size:
        <input 
            type="hidden" 
            class="${css_class}" 
            kind="${kind}"
            id="${name}" 
            name="${name}"
            value="${bin_data}"/>
    % endif
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
        <a class="button-a" href="javascript: void(0)" onclick="save_binary_data('${name}', '${filename}')">${_("Save As")}</a>
        % endif
        % if editable and not readonly:
        <a class="button-a" href="javascript: void(0)" onclick="add_binary('${name}')">${_("add attachment")}</a>
        % endif
    </div>
    % if editable and error:
    <span class="fielderror">${error}</span>
    % endif
</div>

