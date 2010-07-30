<%
    name_base = name and (name != '_terp_list' or None) and name + '/'
%>
<div class="pager">
    <p id="_${name+str(pager_id)}_link_span" class="paging">
        % if prev:
        <a href="#first" onclick="pager_action('first', '${name}'); return false;">
        % endif
        <span class="first nav">${_("<< First")}</span>
        % if prev:
        </a>
        <a href="#previous" onclick="pager_action('previous', '${name}'); return false;">
        % endif
        <span class="prev nav">${_("< Previous")}</span>
        % if prev:
        </a>
        % endif
        <span onclick="jQuery('[id=_${name+str(pager_id)}_link_span]').hide(); jQuery('[id=_${name+str(pager_id)}_limit_span]').show();">${page_info}</span>
        % if next:
        <a href="#next" onclick="pager_action('next', '${name}'); return false;">
        % endif
        <span class="next nav">${_("Next >")}</span>
        % if next:
        </a>
        <a href="#last" onclick="pager_action('last', '${name}'); return false;">
        % endif
        <span class="last nav">${_("Last >>")}</span>
        % if next:
        </a>
        % endif
    </p>

    <div id="_${name+str(pager_id)}_limit_span" style="display: none" align="right">
        <label for="_${name+str(pager_id)}_limit"
               onclick="jQuery('[id=_${name+str(pager_id)}_limit_span]').hide(); jQuery('[id=_${name+str(pager_id)}_link_span]').show();">${_("Change Limit:")}</label>&nbsp;
        <select id='_${name+str(pager_id)}_limit'
                onchange="jQuery('[id=${name_base}_terp_limit]').val(jQuery(this).val());
                          jQuery('[id=${name_base}_terp_offset]').val(0);
                      pager_action('filter', '${name}')" style="min-width: 25px;">
            <option value=""></option>
            % for k in pager_options:
                <option value="${k}" ${py.selector(limit=='${k]}')}>${k}</option>
            %endfor
            <option value="-1" ${py.selector(limit==-1)}>unlimited</option>
        </select>
    </div>
</div>
