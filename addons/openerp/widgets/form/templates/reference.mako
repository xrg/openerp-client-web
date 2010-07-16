% if editable:
    <table width="100%" class="reference" cellpadding="0" cellspacing="0">
        <tr>
            <td nowrap="nowrap" width="1%">
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
            <td nowrap="nowrap" width="20%" align="left">
                <table>
                    <tr>
                        <td>
                            <input type="text" id='${name}_text' class="${css_class}" ${py.attrs(attrs, kind=kind, relation=relation, value=text)}/>
			                % if error:
			                <span class="fielderror">${error}</span>
			                % endif
                        </td>
                        % if not inline:
				            <td width="16" style="padding-left: 2px" nowrap="nowrap">
				                <img id='${name}_open' 
				                    width="16" 
				                    height="16" 
				                    alt="${_('Open')}" 
				                    title="${_('Open a resource')}" 
				                    src="/openerp/static/images/stock/gtk-open.png" 
				                    style="cursor: pointer;" 
				                    class="imgSelect"/>
				            </td>
                        % endif
                        <td width="16" style="padding-left: 2px" nowrap="nowrap">
                            <img id='${name}_select' width="16" height="16" alt="${_('Search')}" title="${_('Search')}" src="/openerp/static/images/stock/gtk-find.png" style="cursor: pointer;" class="imgSelect"/>
                        </td>
                    </tr>
                </table>
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

