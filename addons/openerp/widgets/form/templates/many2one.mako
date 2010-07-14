% if editable:
<div>
    <input type="hidden" id="${name}" name="${name}" class="${css_class}" value="${value}"
        ${py.attrs(attrs, kind=kind, domain=domain, context=ctx, relation=relation)}/>
    <input type="text" id="${name}_text" class="${css_class}"
        ${py.attrs(attrs, kind=kind, relation=relation, value=text)}/>
       
    <input type="hidden" id="_hidden_${name}" value=""/>
    <div id="autoCompleteResults_${name}" class="autoTextResults"></div>
    % if error:
    <span class="fielderror">${error}</span>
    % endif

    % if not inline:
    <img id="${name}_select" alt="${_('Search')}" title="${_('Search')}"
        src="/openerp/static/images/fields-a-lookup-a.gif" class="${css_class} m2o_select"/>
	<img id="${name}_open" alt="${_('Open')}" title="${_('Open a resource')}"
	   src="/openerp/static/images/iconset-d-drop.gif" class="m2o_open"/>
	% endif
</div>
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

% if default_focus:
	<script type="text/javascript">
	    jQuery('#${name}_text').focus()
	</script>
% endif
