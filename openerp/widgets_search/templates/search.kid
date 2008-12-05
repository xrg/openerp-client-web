<table class="fields" border="0" width="100%" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td>
            <div class="tabber" id="search_view_notebook">
                <div class="tabbertab" title="${_('Basic Search')}">
                      <span py:replace="basic.display(value_for(basic), **params_for(basic))" py:if="basic"/>
                </div>
                <div class="tabbertab" title="${_('Advanced Search')}">
                    <span py:replace="advance.display(value_for(advance), **params_for(advance))" py:if="advance"/>
                </div>
            </div>
        </td>
    </tr>
</table>
