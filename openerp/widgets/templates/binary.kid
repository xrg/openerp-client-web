<table xmlns:py="http://purl.org/kid/ns#" border="0" cellpadding="0">
    <tr>
        <td>
            <div id="${name}_binary_add" style="display: none;">
                <input py:if="editable and not readonly and not filename" py:attrs="attrs"
                    type="file" 
                    class="${field_class}"
                    kind="${kind}"
                    disabled="disabled" 
                    id="${name}"
                    name="${name}"/>
                <input py:if="editable and filename and not readonly" py:attrs="attrs"
                    type="file" 
                    class="${field_class}" 
                    kind="${kind}"
                    disabled="disabled" 
                    id="${name}" 
                    name="${name}"/>
            </div>
            <div id="${name}_binary_buttons" style="white-space: nowrap;">
                <span py:content="value or text"/>
                <button py:if="editable and not text" type="button" onclick="add_binary('${name}')">Add</button>
                <button py:if="text" type="button" onclick="save_binary_data('${name}', '${filename}')">Save As</button>
                <button py:if="text and not readonly and editable" type="button" 
                    onclick="submit_form('clear_binary_data?_terp_field=${name}&amp;_terp_fname=${filename}')">Clear</button>
            </div>
            <span py:if="editable and error" class="fielderror" py:content="error"/>
        </td>
     </tr>
 </table>
