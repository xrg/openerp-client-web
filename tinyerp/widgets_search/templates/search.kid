<table width="100%" border="0" cellpadding="5" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td valign="top">
	        <h1 id="icon_list">
				<div class="button_right">
					<button id="icon_list">SEARCH</button>
					<button id="icon_list">EDIT</button>
					<button id="icon_list" class="inactive">GRAPH</button>
				</div>
				${form_view.string}
			</h1>
			${form_view.display(value_for(form_view), **params_for(form_view))}
			<h2 id="icon_list">${list_view.string} list</h2>
			${list_view.display(value_for(list_view), **params_for(list_view))}		
        </td>
    </tr>  		
</table>  	
