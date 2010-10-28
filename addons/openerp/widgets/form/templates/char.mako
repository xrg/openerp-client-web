% if editable:
    <span class="char">
        <input type="${password and 'password' or 'text'}"
            id="${name}" name="${name}" class="${css_class}"
            ${py.attrs(attrs, kind=kind, maxlength=size, value=value)}/>
        % if translatable:
            <img id="0" relation="${model}" src="/openerp/static/images/stock/stock_translate.png" class="translatable" />
            <script type="text/javascript">
                jQuery('img.translatable').click(function() {
                    var translate_links = jQuery('a[xid=translate_fields]');
                    if (translate_links.length) {
                        translate_fields(translate_links[0]);
                    }
                });
            </script>
        % endif
        % if error:
            <span class="fielderror">${error}</span>
        % endif
    </span>
% endif

% if not editable and not password:
    <span kind="${kind}" id="${name}" value="${value}">${value}</span>
% endif

% if not editable and password and value:
    <span>${'*' * len(value)}</span>
% endif

