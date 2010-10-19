% if editable:
<table class="item-wrapper reference">
<tr>
    <td>
        <input type="hidden" id='${name}' name='${name}' class="${css_class}"
                ${py.attrs(attrs, kind=kind, domain=domain, context=ctx, relation=relation, value=value)}/>
        <select id="${name}_reference" name='${name}'>
            <option value=""></option>
            % for (k, v) in options:
                % if relation == k:
            <option value="${k}" selected="1">${v}</option>
                % endif
            % endfor
            % for (k, v) in options:
                % if relation != k:
            <option value="${k}">${v}</option>
                % endif
            % endfor
        </select>
    </td>
    <td>
        <div class="m2o_container">
            <span class="m2o">
                <input type="text" id='${name}_text' class="${css_class}"
                ${py.attrs(attrs, kind=kind, relation=relation, value=text)}/>
                % if error:
                    <span class="fielderror">${error}</span>
                % endif
                % if not inline:
                    <img id="${name}_select" alt="${_('Search')}" title="${_('Search')}"
                        src="/openerp/static/images/fields-a-lookup-a.gif" class="${css_class} m2o_select" style="right: 18px;"/>
                % endif
                <img id="${name}_open" alt="${_('Open')}" title="${_('Open a resource')}"
                src="/openerp/static/images/iconset-d-drop.gif" class="m2o_open"/>
            </span>
        </div>
    </td>
</tr>
</table>
% endif

% if editable:
    <script type="text/javascript">
        new ManyToOne('${name}');
    </script>
% else:
    <span>
        <span id="${name}" ${py.attrs(kind=kind, value=value, relation=relation)}>
            <a style="color:#9A0404;" href="${py.url('/openerp/form/view', model=relation, id=value)}">${text}</a>
        </span>
    </span>
% endif

