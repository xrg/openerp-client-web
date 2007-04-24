<span xmlns:py="http://purl.org/kid/ns#" >
    <table>
        <tr>
            <td>
                <input type="file" py:attrs="attrs" id="${name}" name="${name}" py:if="value is None" />      
                ${value}
            </td>
            <td>                
                <button type="submit" py:attrs="attrs" onclick="submit_form('save_binary?field_search=${name}')">Save As</button>
    		    <button type="submit" onclick="submit_form('clear_binary?field_search=${name}')" >Clear</button>
	        </td>
        </tr>
     </table>		          
	 <span class="fielderror" py:if="error" py:content="error"/>
</span>