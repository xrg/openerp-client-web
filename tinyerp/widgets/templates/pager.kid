<div class="pager" xmlns:py="http://purl.org/kid/ns#">
    <span id="_${name+str(pager_id)}_link_span">
        <a href="javascript: void(0)" py:strip="not prev" onclick="pager_action('first', '${name}'); return false;"><span>&lt;&lt; First</span></a>
        <a href="javascript: void(0)" py:strip="not prev" onclick="pager_action('previous', '${name}'); return false;"><span>&lt; Previous</span></a>
        <a href="javascript: void(0)" onclick="$('_${name+str(pager_id)}_link_span').style.display='none'; $('_${name+str(pager_id)}_limit_span').style.display=''">${page_info}</a>
        <a href="javascript: void(0)" py:strip="not next" onclick="pager_action('next', '${name}'); return false;"><span>Next &gt;</span></a>
        <a href="javascript: void(0)" py:strip="not next" onclick="pager_action('last', '${name}'); return false;"><span>Last &gt;&gt;</span></a>
    </span>

    <table id="_${name+str(pager_id)}_limit_span" style="display: none" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td align="right">
                <a href="javascript: void(0)" onclick="$('_${name+str(pager_id)}_limit_span').style.display='none'; $('_${name+str(pager_id)}_link_span').style.display=''">Change Limit:</a>&nbsp;
            </td>
            <td>
                <select id='_${name+str(pager_id)}_limit' onchange="$('${name and (name != '_terp_list' or None) and name + '/'}_terp_limit').value=$('_${name+str(pager_id)}_limit').value; pager_action('filter', '${name}')">
                    <option value="20" selected="${tg.selector(limit==20)}">20</option>
                    <option value="40" selected="${tg.selector(limit==40)}">40</option>
                    <option value="60" selected="${tg.selector(limit==60)}">60</option>
                    <option value="80" selected="${tg.selector(limit==80)}">80</option>
                    <option value="100" selected="${tg.selector(limit==100)}">100</option>
                </select>
            </td>
        </tr>
    </table>
</div>
