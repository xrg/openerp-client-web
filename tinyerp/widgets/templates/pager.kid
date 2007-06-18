<div class="pager" xmlns:py="http://purl.org/kid/ns#">    
    <span id="_${pager_id}_link_span">
        <a href="javascript: void(0);" py:strip="not prev" onclick="submit_search_form('first'); return false;">&lt;&lt; First</a>
        <a href="javascript: void(0);" py:strip="not prev" onclick="submit_search_form('previous'); return false;">&lt; Previous</a>
        <a href="javascript: void(0);" onclick="$('_${pager_id}_link_span').style.display='none'; $('_${pager_id}_limit_span').style.display=''">${page_info}</a>
        <a href="javascript: void(0);" py:strip="not next" onclick="submit_search_form('next'); return false;">Next &gt;</a>
        <a href="javascript: void(0);" py:strip="not next" onclick="submit_search_form('last'); return false;">Last &gt;&gt;</a>
    </span>
    
    <span id="_${pager_id}_limit_span" style="display: none">
        Change Limit: 
        <select id='_${pager_id}_limit' onchange="$('_terp_limit').value=$('_${pager_id}_limit').value; submit_search_form('filter')">
            <option selected="${tg.selector(limit==20)}">20</option>
            <option selected="${tg.selector(limit==40)}">40</option>
            <option selected="${tg.selector(limit==60)}">60</option>
            <option selected="${tg.selector(limit==80)}">80</option>
            <option selected="${tg.selector(limit==100)}">100</option>
        </select>
    </span>
</div>
