<form xmlns:py="http://purl.org/kid/ns#" method="post" id="${name}" name="${name}" action="${action}" enctype="multipart/form-data">
    <input type="hidden" value="${limit}" name="_terp_limit" id="_terp_limit"/>
    <input type="hidden" value="${offset}" name="_terp_offset" id="_terp_offset"/>
    <input type="hidden" value="${count}" name="_terp_count" id="_terp_count"/>
    <input type="hidden" id="_terp_search_domain" name="_terp_search_domain" value="${ustr(search_domain)}"/>
    <input type="hidden" id="_terp_search_data" name="_terp_search_data" value="${ustr(search_data)}"/>
    
    <span py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
    
    <table border="0" cellpadding="0" cellspacing="0" width="100%" py:if="screen">
            <tr>
                <td valign="top" width="100%" py:if="search" py:content="search.display(value_for(search), **params_for(search))"></td>
            </tr>
            <tr>
                <td py:if="search" style="padding: 3px; padding-top: 0px">                    
                    <div class="toolbar">                        
                        <button type="button" onclick="submit_search_form('find')">Find</button>
                        <button type="button" onclick="submit_form('new')">New</button>
                    </div>                    
                </td>
            </tr>
            <tr>
                <td valign="top" width="100%" py:content="screen.display(value_for(screen), **params_for(screen))"></td>
            </tr>
    </table>
</form>
