<style type="text/css">
	
</style>
% if editable:
    <table id="m2o_table" cellpadding="0" cellspacing="0" style="width: auto;">
    
        <tr>
            <td id="m2o" style="border-right: none; padding: 0;">
                <input type="hidden" id="${name}" name="${name}" class="${css_class}" value="${value}"
                    ${py.attrs(attrs, kind=kind, domain=domain, context=ctx, relation=relation)}/>
                <input type="text" id="${name}_text" class="${css_class}"
                    ${py.attrs(attrs, kind=kind, relation=relation, value=text)} style="width: 100px; position: relative; height: 17px; border-right: none;"/>
                   
                <input type="hidden" id="_hidden_${name}" value=""/>
                <div id="autoCompleteResults_${name}" class="autoTextResults"></div>
                % if error:
                <span class="fielderror">${error}</span>
                % endif
            </td>
            <td id="m2o" style="border-left: none; padding: 0;">
                <img id="${name}_select" class="m2o_select" src="/openerp/static/images/fields-a-lookup-a.jpg" title="${_('Search')}" alt="${_('Search')}"/>
            </td>
            <td>                           
            	<img id="${name}_open" src="/openerp/static/images/iconset-d-drop.gif" alt="${_('Open')}" title="${_('Open a resource')}"/>
            </td>
            
        </tr>
    </table>
% endif

% if editable:
    <script type="text/javascript">
        new ManyToOne('${name}');
    </script>
% endif

% if not editable and link:
    % if link=='1':
        <span id="${name}" ${py.attrs(kind=kind, value=value)}>
            <a href="${py.url('/openerp/form/view', model=relation, id=value)}">${text}</a>
        </span>
    % endif
    % if link=='0':
        <span id="${name}" ${py.attrs(kind=kind, value=value)}>${text}</span>
    % endif
% endif

% if not editable and not link == '0':
    <span>
        <span id="${name}" ${py.attrs(kind=kind, value=value, relation=relation)}>
            <a href="${py.url('/openerp/form/view', model=relation, id=value)}">${text}</a>
        </span>
    </span>
% endif

