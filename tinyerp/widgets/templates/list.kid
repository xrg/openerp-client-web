<table id="${name}" class="grid" width="100%" cellspacing="0" cellpadding="0" xmlns:py="http://purl.org/kid/ns#">
	<tr py:if="pageable">
	    <td>
	        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="pager">
	            <tr>
	                <td align="right">
						<a href="#" class="arrow_link"><img border="0" src="/static/images/newstarticon.gif"/> Start</a>   
						<a href="#" class="arrow_link"><img border="0" src="/static/images/newpericon.gif"/> Previous</a>    
						<a href="#" class="arrow_link">(1-5)</a>    
						<a href="#" class="arrow_link">Next <img border="0" src="/static/images/newnexticon.gif"/></a>   
						<a href="#" class="arrow_link">End <img border="0" src="/static/images/newendicon.gif"/></a>   
					</td>			                
	            </tr>
	        </table>
	    </td>
	</tr>
	<tr>
	    <td>
			<table width="100%" cellpadding="0" cellspacing="0">
			    <thead>
			        <tr>
			            <th width="1%" py:if="selectable">
			                <input type="checkbox" class="checkbox" py:if="selector=='checkbox'" onclick="new ListView('${name}').checkAll(this.checked)"/>
			            </th>
			            <th py:for="field in headers" py:content="field[1]">Title</th>
			            <th align="center" width="20px" py:if="editable"></th>
			            <th align="center" width="20px" py:if="editable"></th>
			        </tr>
			    </thead>
			    <tbody>
			        <tr py:for="i, row in enumerate(data)" class="row">
		
			            <td width="1%" py:if="selectable">
			                <input type="${selector}" class="${selector}" id="${name}/${row['id']}" name="${name}" value="${row['id']}"/>
			            </td>
			            <td py:for="field, title in headers" py:content="row[field]">Data</td>
			            <td py:if="editable" style="text-align: center">
			                <img src="/static/images/edit_inline.gif" class="listImage" border="0" title="Edit" onclick="inlineEdit(${row['id']}, '${source}')"/>
			            </td>
			            <td py:if="editable" style="text-align: center">
			                <img src="/static/images/delete_inline.gif" class="listImage" border="0" title="Delete" onclick="inlineDelete(${row['id']}, '${source}')"/>
			            </td>
			        </tr>
		
			        <tr py:if="not data" py:for="i in range(6)" class="row">
			            <td align="center" py:if="selectable"></td>
			            <td py:for="field, title in headers">&nbsp;</td>
			            <td py:if="editable" style="text-align: center">
			            </td>
			            <td py:if="editable" style="text-align: center">
			            </td>
			        </tr>
			    </tbody>
			</table>			        
	    </td>
	</tr>    
	<tr py:if="pageable">
	    <td>
	        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="pager">
	            <tr>		            			        
					<td>		 
						<a href="#">Import</a> |
						<a href="#">Export</a>
					</td>
					<td align="right">
						<a href="#"><img border="0" src="/static/images/newstarticon.gif"/> Start</a>   
						<a href="#"><img border="0" src="/static/images/newpericon.gif"/> Previous</a>    
						<a href="#">(1-5)</a>    
						<a href="#">Next <img border="0" src="/static/images/newnexticon.gif"/></a>   
						<a href="#">End <img border="0" src="/static/images/newendicon.gif"/></a>   
					</td>
                </tr>
            </table>
        </td>
	</tr>
</table>