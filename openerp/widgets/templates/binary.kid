<table xmlns:py="http://purl.org/kid/ns#" border="0" cellpadding="0">
    <tr>
        <td>
            <div id="${name}_binary_add" style="display: None;">
                <input py:if="editable and not readonly and not filename" nowrap="nowrap" type="file" class="${field_class}" py:attrs="attrs" disabled="disabled" id="${name}" name="${name}"/>
                <input py:if="editable and filename and not readonly" type="file" class="${field_class}" py:attrs="attrs" disabled="disabled" id="${name}" name="${name}" onchange="set_binary_filename(('${filename}'), this);"/>
            </div>
            <div id="${name}_binary_buttons">
                <table>
                    <tr>
                        <td py:if="editable and text is None" width="75px">
                            <button type="button" onclick="add_binary('${name}')">Add</button>
                        </td>
                        <td py:if="text is not None and editable" width="75px">
                            <button type="button" onclick="save_binary_data('${name}', '${filename}')">Save As</button>
                        </td>
                        <td py:if="text is not None and editable" width="1px"></td>
                        <td py:if="text is not None and not readonly and editable" width="75px">
                            <button type="button" onclick="submit_form('clear_binary_data?_terp_field=${name}&amp;_terp_fname=${filename}')">Clear</button>
                        </td>
                        <span py:if="editable and error" class="fielderror" py:content="error"/>
                        <td py:if="not editable">
                            <span py:content="value or text"/>
                            <td width="75px" py:if="value or text">
                                <button type="button" onclick="save_binary_data('${name}', '${filename}')">Save As</button>
                            </td>
                        </td>
                    </tr>
                </table>
            </div>
        </td>
     </tr>
 </table>
