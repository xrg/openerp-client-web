<table id="${name}" class="grid" width="100%" cellspacing="0" cellpadding="0" xmlns:py="http://purl.org/kid/ns#">
	<tr class="pager" py:if="pageable">
	    <td colspan="${columns}">
	        <table border="0" cellpadding="0" cellspacing="0" width="100%">
	            <tr>
	                <td align="right">
	                    
	                    <span py:if="(offset&lt;0) or (offset is 0)" class="disabled_text">
						    <img border="0" align="absmiddle" src="/static/images/first_off.gif"/> Start
						</span>
						<span py:if="(offset&gt;0)">
						    <a href="javascript: void(0)" onclick="submit_search_form('first'); return false;">
						        <img border="0" align="absmiddle" src="/static/images/pager_start.gif"/> <b>Start</b>
						    </a>
						</span>    
						
						<span py:if="(offset&lt;0) or (offset is 0)" class="disabled_text">
						    <img border="0" align="absmiddle" src="/static/images/previous_off.gif"/> Previous
						</span>
						<span py:if="(offset&gt;0)">
						    <a href="javascript: void(0)" onclick="submit_search_form('previous'); return false;">
						        <img border="0" align="absmiddle" src="/static/images/pager_prev.gif"/> <b>Previous</b>
						    </a>
                        </span>
                        						    
						<a href="javascript: void(0)" py:strip="">(${offset} to ${len(data) + offset})</a>
						
						<span py:if="(len(data)&lt;limit)" class="disabled_text">
                            Next <img border="0" align="absmiddle" src="/static/images/next_off.gif"/>
						</span>
                        <span py:if="(len(data)&gt;limit) or (len(data) is limit)">
       						<a href="javascript: void(0)" onclick="submit_search_form('next'); return false;">
       						    <b>Next</b> <img border="0" align="absmiddle" src="/static/images/pager_next.gif"/>
       						</a>
                        </span>
                        
                        <span py:if="(len(data)&lt;limit)" class="disabled_text">
                            End <img border="0" align="absmiddle" src="/static/images/end_off.gif"/>
						</span>						
						<span py:if="(len(data)&gt;limit) or (len(data) is limit)">
    						<a href="javascript: void(0)" onclick="submit_search_form('last'); return false;">
    						    <b>End </b><img border="0" align="absmiddle" src="/static/images/pager_end.gif"/>
    						</a>
    				    </span>
    				    
					</td>
	            </tr>
	        </table>
	    </td>
	</tr>

    <tr class="header">
        <td width="1%" py:if="selectable">
            <input type="checkbox" class="checkbox" py:if="selector=='checkbox'" onclick="new ListView('${name}').checkAll(this.checked)"/>
        </td>
        <td py:for="(field, field_attrs) in headers" py:content="field_attrs['string']">Title</td>
        <td align="center" width="10px" py:if="editable"></td>
        <td align="center" width="10px" py:if="editable"></td>
    </tr>

    <tr py:for="i, row in enumerate(data)" class="row">
        <td width="1%" py:if="selectable">
            <input type="${selector}" class="${selector}" id="${name}/${row['id']}" name="${name}" value="${row['id']}"/>
        </td>
        <td py:for="i, (field, field_attrs) in enumerate(headers)">
            <a py:strip="(show_links &lt; 0 or (i > 0 and show_links==0)) or not row[field].link" href="${row[field].link}" onclick="${row[field].onclick}">${row[field]}</a>
        </td>
        <td py:if="editable" style="text-align: center">
            <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="Edit" onclick="inlineEdit(${row['id']}, '${source}')"/>
        </td>
        <td py:if="editable" style="text-align: center">
            <img src="/static/images/delete_inline.gif" class="listImage" border="0" title="Delete" onclick="inlineDelete(${row['id']}, '${source}')"/>
        </td>                
        
    </tr>
    
    <tr py:for="i in range(0, 4 - len(data))" class="row">
        <td width="1%" py:if="selectable">&nbsp;</td>
        <td py:for="i, (field, field_attrs) in enumerate(headers)">&nbsp;</td>
        <td py:if="editable" style="text-align: center">&nbsp;</td>
        <td py:if="editable" style="text-align: center">&nbsp;</td>        
    </tr>

	<tr class="pager" py:if="pageable">
	    <td colspan="${columns}">
	        <table border="0" cellpadding="0" cellspacing="0" width="100%">
	            <tr>
					<td>		 
						<a href="#">Import</a> |
						<a href="#">Export</a>
					</td>
	                <td align="right">
						<span py:if="(offset&lt;0) or (offset is 0)" class="disabled_text">
						    <img border="0" align="absmiddle" src="/static/images/first_off.gif"/> Start
						</span>
						<span py:if="(offset&gt;0)">
						    <a href="javascript: void(0)" onclick="submit_search_form('first'); return false;">
						        <img border="0" align="absmiddle" src="/static/images/pager_start.gif"/> <b>Start</b>
						    </a>
						</span>    
						
						<span py:if="(offset&lt;0) or (offset is 0)" class="disabled_text">
						    <img border="0" align="absmiddle" src="/static/images/previous_off.gif"/> Previous
						</span>
						<span py:if="(offset&gt;0)">
						    <a href="javascript: void(0)" onclick="submit_search_form('previous'); return false;">
						        <img border="0" align="absmiddle" src="/static/images/pager_prev.gif"/> <b>Previous</b>
						    </a>
                        </span>
                        						    
						<a href="javascript: void(0)" py:strip="">(${offset} to ${len(data) + offset})</a>
						
						<span py:if="(len(data)&lt;limit)" class="disabled_text">
                            Next <img border="0" align="absmiddle" src="/static/images/next_off.gif"/>
						</span>
                        <span py:if="(len(data)&gt;limit) or (len(data) is limit)">
       						<a href="javascript: void(0)" onclick="submit_search_form('next'); return false;">
       						    <b>Next </b><img border="0" align="absmiddle" src="/static/images/pager_next.gif"/>
       						</a>
                        </span>
                        
                        <span py:if="(len(data)&lt;limit)" class="disabled_text">
                            End <img border="0" align="absmiddle" src="/static/images/end_off.gif"/>
						</span>
						
						<span py:if="(len(data)&gt;limit) or (len(data) is limit)">
    						<a href="javascript: void(0)" onclick="submit_search_form('last'); return false;">
    						    <b>End </b><img border="0" align="absmiddle" src="/static/images/pager_end.gif"/>
    						</a>
    				    </span>
					</td>
                </tr>
            </table>
        </td>
	</tr>
</table>
