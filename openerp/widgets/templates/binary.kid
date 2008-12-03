<table xmlns:py="http://purl.org/kid/ns#" border="0" cellpadding="0">
    <tr>
        <td>
            <div id="binary_add" style="display: None;">
                <table>
                    <tr>
                        <td py:if="editable and not readonly and not filename" nowrap="nowrap">
                            <input type="file" class="${field_class}" py:attrs="attrs" disabled="disabled" id="${name}" name="${name}" py:if="editable"/>
                        </td>
                        <td py:if="editable and filename and not readonly">
                            <input type="file" class="${field_class}" py:attrs="attrs" disabled="disabled" id="${name}" name="${name}" py:if="editable" onchange="set_binary_filename(('${filename}'), this);"/>
                        </td>
                    </tr>
                </table>
            </div>
            <div id="binary_buttons">
                <table>
                    <tr>
                        <td py:if="editable" width="75px">
                            <button type="button" onclick="add_binary('${name}', '${filename}')">Add</button>
                        </td>
                        <td py:if="text is not None and editable" width="75px">
                            <button type="button" onclick="save_binary_data('${name}', '${filename}')">Save As</button>
                        </td>
                        <td py:if="text is not None and editable" width="1px"><div class="spacer"/></td>
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
