% if editable:
    <span class="char">
        <input type="${password and 'password' or 'text'}"
            id="${name}" name="${name}" class="${css_class}"
            ${py.attrs(attrs, kind=kind, maxlength=size, value=value)}/>
        % if translatable:
            <img src="/openerp/static/images/stock/stock_translate.png" class="translatable" />
            <script type="text/javascript">
                jQuery('img.translatable').click(function() {
                    var params = {
                        'relation': '${model}',
                        'id': jQuery('#_terp_id').attr('value'),
                        'data': jQuery('#_terp_context').attr('value'),
                    };
                    translate_fields(null, params);
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

