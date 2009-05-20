<table class="fields" border="0" width="100%">
    <tr>
        <td>
            <div class="tabber" id="search_view_notebook">
                <div class="tabbertab" title="${_('Basic Search')}">
                    % if basic:
                        ${display_member(basic)}
                    % endif
                </div>
                <div class="tabbertab" title="${_('Advanced Search')}">
                    % if advance:
                        ${display_member(advance)}
                    % endif
                </div>
            </div>
            <script type="text/javascript">
                tabberOptions.div = getElement('search_view_notebook');
                tabberOptions.div.tabber = new tabberObj(tabberOptions);
            </script>
        </td>
    </tr>
</table>

