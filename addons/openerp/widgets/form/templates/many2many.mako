<table border="0" width="100%" id="_m2m_${name}" class="many2many m2m_box" detail="${inline}" relation="${relation}" ${py.attrs(attrs, domain=domain, context=ctx)}>
    % if editable:
    <tr>
        <td style="display:none;">
        	% if inline:
	            <input type="hidden" class="${css_class}" kind="${kind}" id='${name}_id' value="${screen.ids}" ${py.attrs(attrs)} relation="${relation}"/>
	            <input type="hidden" kind="${kind}" name="${name}" id="${name}" value="${screen.ids}" relation="${relation}"/>
	            <input type="hidden" class="${css_class}" value="(${len(screen.ids or [])})" readonly="0" id='${name}_set' kind="${kind}" ${py.attrs(attrs)} style="width: 100%; text-align: center;"/>
            % else:
            	<input type="hidden" class="${css_class}" id='${name}_set' kind="${kind}" ${py.attrs(attrs)} style="width: 100%;"/>
            % endif
            % if error:
            	<span class="fielderror">${error}</span>
            % endif
		</td>
    </tr>
    % endif
    % if not inline:
    <tr>
        % if screen:
    	<td id='${name}_container' class="m2m_cell">
            ${screen.display()}
            <!-- IMP: IE problem, openobject.dom.get('some_name') returns field with name="some_id" instead of id="some_id" -->
            % if not editable:
                <input type="hidden" class="${css_class}" id='${name}_set' kind="${kind}" ${py.attrs(attrs)} style="width: 100%;"/>
            % endif
            <input type="hidden" class="${css_class}" kind="${kind}" id='${name}_id' name="${name}" value="${screen.ids}" ${py.attrs(attrs)} relation="${relation}"/>
        </td>
        % endif
    </tr>
    % endif

    % if editable:
    <script type="text/javascript">
        new Many2Many('${name}');
    </script>
    % endif
    
</table>

