<%def name="display_open_resource(name)">
    <img id="${name}_open" alt="${_('Open')}" title="${_('Open a resource')}"
        src="/openerp/static/images/iconset-d-drop.gif" class="m2o_open"/>
</%def>
<%def name="m2o_container()">
    <div class="m2o_container">
        ${caller.body()}
    </div>
</%def>
% if editable:
    <%self:m2o_container>
        <span class="m2o">
            <input type="hidden" id="${name}" name="${name}" class="${css_class}" value="${value}"
                ${py.attrs(attrs, kind=kind, domain=domain, context=ctx, relation=relation)}/>
            <input type="text" id="${name}_text" class="${css_class}" name="${name}"
                ${py.attrs(attrs, kind=kind, relation=relation, value=text)}/>

            <input type="hidden" id="_hidden_${name}" value=""/>
            % if error:
                <span class="fielderror">${error}</span>
            % endif
            <img id="${name}_select" alt="${_('Search')}" title="${_('Search')}"
                src="/openerp/static/images/fields-a-lookup-a.gif" class="m2o_select"/>
        </span>
        ${self.display_open_resource(name)}
        <div id="autoCompleteResults_${name}" class="autoTextResults"></div>
        <script type="text/javascript">
            new ManyToOne('${name}');
        </script>
    </%self:m2o_container>
% endif

% if not editable and link:
    % if link == '1':
        <span id="${name}" name="${name}" ${py.attrs(kind=kind, value=value, relation=relation, context=ctx, domain=domain, link=link)}>
            <a style="color:#9A0404;" href="javascript: void(0)" onclick="new ManyToOne('${name}').open_record('${value}')">${text}</a>
        </span>
    % elif link == '0':
        <span id="${name}" ${py.attrs(kind=kind, value=value, relation=relation, link=link)}>${text}</span>
    % endif
% endif

% if default_focus:
	<script type="text/javascript">
	    jQuery('#${name}_text').focus()
	</script>
% endif
