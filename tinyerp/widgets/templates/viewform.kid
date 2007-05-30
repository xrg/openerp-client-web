<form xmlns:py="http://purl.org/kid/ns#" method="post" id="${name}" name="${name}" action="${action}" enctype="multipart/form-data">
    <span py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
    <table border="0" cellpadding="0" cellspacing="0" width="100%" py:if="screen">
            <tr><td valign="top" py:if="search" py:content="search.display(value_for(search), **params_for(search))" width="100%"></td></tr>
            <tr>
                <td py:if="search">
                    <div class="spacer"/>
                    <div class="toolbar">
                        <button type="button" onclick="submit_search_form()">Find</button>
                    </div>
                    <div class="spacer"/>
                </td>
            </tr>
            <tr><td valign="top" width="100%" py:content="screen.display(value_for(screen), **params_for(screen))"></td></tr>
    </table>
</form>
