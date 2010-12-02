<select ${py.attrs(attrs)} class="${css_class}">
    % for group, options in grouped_options:
        % if group:
            <optgroup label="${group}">
        % endif
        % for val, desc, _attrs in options:
            <option value="${val}" ${py.attrs(_attrs)}>${desc}</option>
        % endfor
        % if group:
            </optgroup>
        % endif
    % endfor
</select>
