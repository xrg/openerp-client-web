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
                % if 'requiredfield' in css_class:
                    <input id="${name}_open" class="${css_class}" type="image" src="/openerp/static/images/fields-a-lookup-a-require.jpg" size="16,16" alt="${_('Open')}" style="height: 17px; text-align: right; margin-left: -3px; border-left: none;" title="${_('Open a resource')}"/>
                % else:
                    <input id="${name}_open" class="${css_class}" type="image" src="/openerp/static/images/fields-a-lookup-a.jpg" size="16,16" alt="${_('Open')}" style="height: 17px; text-align: right; margin-left: -3px; border-left: none;" title="${_('Open a resource')}"/>
           	   % endif
            </td>
            <td>
            	<img id='${name}_select' style="cursor: pointer;" src="/openerp/static/images/iconset-d-drop.gif" alt="${_('Search')}" title="${_('Search')}"/>
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
        <span id="${name}" name="${name}" ${py.attrs(kind=kind, value=value, relation=relation, context=ctx, domain=domain, link=link)}>
            <a href="javascript: void(0)" onclick="new ManyToOne('${name}').open_record('${value}')">${text}</a>
        </span>
    % endif
    % if link=='0':
        <span id="${name}" ${py.attrs(kind=kind, value=value, relation=relation, link=link)}>${text}</span>
    % endif
% endif

