<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <table py:if="editable" border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td>
                <input type="file" class="${field_class}" py:attrs="attrs" id="${name}" name="${name}" py:if="text is None"/>${text}
            </td>

            <td py:if="text is not None" width="75px">
                <button type="submit" onclick="submit_form('save_binary?field_search=${name}')">Save As</button>
            </td>
            <td py:if="text is not None" width="1px"><div class="spacer"/></td>    
            <td py:if="text is not None" width="75px">
                <button type="submit" onclick="submit_form('clear_binary?field_search=${name}')">Clear</button>                
            </td>            
        </tr>
     </table>		          
	 <span py:if="editable and error" class="fielderror" py:content="error"/>
     <span py:if="not editable" py:content="value"/>
</span>