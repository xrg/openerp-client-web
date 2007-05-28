<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <table py:if="editable" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <input type="file" py:attrs="attrs" id="${name}" name="${name}" py:if="value is None"/>${value}
            </td>
            <td>                
                <button type="submit" py:attrs="attrs" onclick="submit_form('save_binary?field_search=${name}')" py:if="value is not None">Save As</button>
    		    <button type="submit" onclick="submit_form('clear_binary?field_search=${name}')" py:if="value is not None">Clear</button>
	        </td>
        </tr>
     </table>		          
	 <span py:if="editable and error" class="fielderror" py:content="error"/>
     <span py:if="not editable" py:content="value"/>
</span>