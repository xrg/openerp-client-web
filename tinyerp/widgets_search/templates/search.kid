<table width="100%" border="0" cellpadding="5" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td>
            <table width="100%" class="titlebar">
                <tr>
                    <td width="32px" align="center">
                        <img src="/static/images/icon.gif"/>
                    </td>
                    <td width="100%" py:content="form_view.string">Form Title</td>
                    <td nowrap="">
                        <button>Search</button>
                        <button>Edit</button>
                        <button>Graph</button>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td valign="top">
			${form_view.display(value_for(form_view), **params_for(form_view))}
		</td>
	</tr>
	<tr>
	    <td>
            <table width="100%" class="titlebar">
                <tr>
                    <td width="32px" align="center">
                        <img src="/static/images/icon.gif"/>
                    </td>
                    <td py:content="list_view.string + ' List'">List Title</td>
                </tr>
            </table>
	    </td>
	</tr>
	<tr>
	    <td>
			${list_view.display(value_for(list_view), **params_for(list_view))}		
        </td>
    </tr>  		
</table>  	
