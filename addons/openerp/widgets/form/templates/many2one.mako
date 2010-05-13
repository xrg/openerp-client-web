<style type="text/css">
	table#m2o_table {
		
	}
	td#m2o {
	padding: 0px;
	border: none;
		border: 1px solid #aaa9a9; 
	border-color: #e5e3e3 #dad9d9 #cccbcb; 
	border-radius: 3px; 
	-moz-border-radius: 3px; 
	-webkit-border-radius: 3px; 
	/* box-shadow: 0 1px 0 #fff; 
	-moz-box-shadow: 0 1px 0 #fff; 
	-webkit-box-shadow: 0 1px 0 #fff; */
	}
	
	td#m2o input {
		padding: 0px;
		border: none;
		border-style: none;
		border-radius: 0px;
		-moz-border-radius: 0px; 
		-webkit-border-radius: 0px; 
	}
</style>
% if editable:
    <table id="m2o_table" cellpadding="0" cellspacing="0" style="width: auto;">
    
        <tr>
            <td id="m2o"  class="${css_class}" style="border-right: none;">
                <input type="hidden" id="${name}" name="${name}" class="${css_class}" value="${value}"
                    ${py.attrs(attrs, kind=kind, domain=domain, context=ctx, relation=relation)}/>
                <input type="text" id="${name}_text" class="${css_class}"
                    ${py.attrs(attrs, kind=kind, relation=relation, value=text)} style="width: 100px; position: relative; height: 17px;"/>
                   
                <input type="hidden" id="_hidden_${name}" value=""/>
                <div id="autoCompleteResults_${name}" class="autoTextResults"></div>
                % if error:
                <span class="fielderror">${error}</span>
                % endif
            </td>
            <td id="m2o" class="${css_class}" style="border-left: none;">
            	<input id="${name}_open" class="${css_class}" type="image" src="/openerp/static/images/fields-a-lookup-a.gif" size="16,16" alt="${_('Open')}" title="${_('Open a resource')}"/>
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
        <span id="${name}" ${py.attrs(kind=kind, value=value)}>
            <a href="${py.url('/form/view', model=relation, id=value)}">${text}</a>
        </span>
    % endif
    % if link=='0':
        <span id="${name}" ${py.attrs(kind=kind, value=value)}>${text}</span>
    % endif
% endif

% if not editable and not link == '0':
    <span>
        <span id="${name}" ${py.attrs(kind=kind, value=value, relation=relation)}>
            <a href="${py.url('/form/view', model=relation, id=value)}">${text}</a>
        </span>
    </span>
% endif

