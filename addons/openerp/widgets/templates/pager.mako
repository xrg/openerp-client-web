<div class="pager">
    <p id="_${name+str(pager_id)}_link_span" class="paging">
        % if prev:
        <a class="first" href="javascript: void(0)" title="${_('First record...')}" onclick="pager_action('first', '${name}'); return false;">
        % endif
        <span class="first">${_("<< First")}</span>
        % if prev:
        </a>
        <a class="prev" href="javascript: void(0)" title="${_('Previous record...')}" onclick="pager_action('previous', '${name}'); return false;">
        % endif
        <span class="prev">${_("< Previous")}</span>
        % if prev:
        </a>
        % endif
        <font onclick="openobject.dom.get('_${name+str(pager_id)}_link_span').style.display='none'; openobject.dom.get('_${name+str(pager_id)}_limit_span').style.display=''" style="cursor: pointer;">${page_info}</font>
        % if next:
        <a class="next" href="javascript: void(0)" title="${_('Next record...')}" onclick="pager_action('next', '${name}'); return false;">
        % endif
        <span class="next">${_("Next >")}</span>
        % if next:
        </a>
        <a class="last" href="javascript: void(0)" title="${_('Last record...')}" onclick="pager_action('last', '${name}'); return false;">
        % endif
        <span class="last">${_("Last >>")}</span>
        % if next:
        </a>
        % endif
    </p>
    <p>
    	<div id="_${name+str(pager_id)}_limit_span" style="display: none" align="right">
    		<a href="javascript: void(0)" onclick="openobject.dom.get('_${name+str(pager_id)}_limit_span').style.display='none'; openobject.dom.get('_${name+str(pager_id)}_link_span').style.display=''">${_("Change Limit:")}</a>&nbsp;
    		<select id='_${name+str(pager_id)}_limit' onchange="openobject.dom.get('${name and (name != '_terp_list' or None) and name + '/'}_terp_limit').value=openobject.dom.get('_${name+str(pager_id)}_limit').value;
    		 $('${name and (name != '_terp_list' or None) and name + '/'}_terp_offset').value= 0;pager_action('filter', '${name}')">
	             <option value=""></option>
	             % for k in pager_options:
	             <option value="${k}" ${py.selector(limit=='${k]}')}>${k}</option>
	             %endfor
	             <option value="-1" ${py.selector(limit==-1)}>unlimited</option>
               </select>
    	</div>
    </p>
</div>
