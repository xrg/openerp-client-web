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
        <input type="text" id='${name}_text' class="${css_class}"
            ${py.attrs(attrs, kind=kind, relation=relation, value=text)}/>
        % if error:
        <span class="fielderror">${error}</span>
	    % endif
	</td>
    % if not inline:
    <td>
        <img id="${name}_select" alt="${_('Search')}" title="${_('Search')}"
            src="/openerp/static/images/fields-a-lookup-a.gif" class="${css_class} m2o_select"/>
    </td>
    % endif
    <td width="18px">
        <img id="${name}_open" alt="${_('Open')}" title="${_('Open a resource')}"
    	    src="/openerp/static/images/iconset-d-drop.gif" class="m2o_open"/>
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
            <a href="${py.url('/openerp/form/view', model=relation, id=value)}">${text}</a>
        </span>
    </span>
% endif

