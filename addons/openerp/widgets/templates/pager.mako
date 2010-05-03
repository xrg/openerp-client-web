<div class="pager">
    <span id="_${name+str(pager_id)}_link_span">
        % if prev:
        <a href="javascript: void(0)" onclick="pager_action('first', '${name}'); return false;">
        % endif
        <span>${_("<< First")}</span>
        % if prev:
        </a>
        <a href="javascript: void(0)" onclick="pager_action('previous', '${name}'); return false;">
        % endif
        <span>${_("< Previous")}</span>
        % if prev:
        </a>
        % endif
        <a href="javascript: void(0)" onclick="openobject.dom.get('_${name+str(pager_id)}_link_span').style.display='none'; openobject.dom.get('_${name+str(pager_id)}_limit_span').style.display=''">${page_info}</a>
        % if next:
        <a href="javascript: void(0)" onclick="pager_action('next', '${name}'); return false;">
        % endif
        <span>${_("Next >")}</span>
        % if next:
        </a>
        <a href="javascript: void(0)" onclick="pager_action('last', '${name}'); return false;">
        % endif
        <span>${_("Last >>")}</span>
        % if next:
        </a>
        % endif
    </span>

    <table id="_${name+str(pager_id)}_limit_span" style="width: 100%; display: none" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td align="right">
                <a href="javascript: void(0)" onclick="openobject.dom.get('_${name+str(pager_id)}_limit_span').style.display='none'; openobject.dom.get('_${name+str(pager_id)}_link_span').style.display=''">${_("Change Limit:")}</a>&nbsp;
            </td>
            <td width="45px;">
                <select id='_${name+str(pager_id)}_limit' onchange="openobject.dom.get('${name and (name != '_terp_list' or None) and name + '/'}_terp_limit').value=openobject.dom.get('_${name+str(pager_id)}_limit').value; 
                	$('${name and (name != '_terp_list' or None) and name + '/'}_terp_offset').value= 0;pager_action('filter', '${name}')">
                    <option value=""></option>
                    % for k in pager_options:
                    <option value="${k}" ${py.selector(limit=='${k]}')}>${k}</option>
                    %endfor
                    <option value="-1" ${py.selector(limit==-1)}>unlimited</option>
                </select>
            </td>
        </tr>
    </table>
</div>

