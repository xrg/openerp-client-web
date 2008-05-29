<table class="fields" border="0" width="100%" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td>
            <div class="tabber" id="search_view_notebook">
                <div class="tabbertab">
                    <h3 class="tabbertabtitle">Basic Search</h3>
                      <span py:replace="basic.display(value_for(basic), **params_for(basic))" py:if="basic"/>
                </div>
                <div class="tabbertab">
                    <h3 class="tabbertabtitle">Advanced Search</h3>
                    <span py:replace="advance.display(value_for(advance), **params_for(advance))" py:if="advance"/>
                </div>
            </div>
        </td>
    </tr>
</table>
