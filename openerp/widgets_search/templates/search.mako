<table class="fields" border="0" width="100%">
    <tr>
        <td>
            <div class="notebook" id="search_view_notebook">
                <div title="${_('Basic Search')}">
                    % if basic:
                        ${display_member(basic)}
                    % endif
                </div>
                <div title="${_('Advanced Search')}">
                    % if advance:
                        ${display_member(advance)}
                    % endif
                </div>
            </div>
            <script type="text/javascript">
                var SEARCH_NOTEBOOK = new Notebook('search_view_notebook', {
                    'closable': false,
                    'remember': true
                });
            </script>
        </td>
    </tr>
</table>

