<dl id="calGroups">
    % if title:
    <dt class="calGroupsTitle">
        <table>
            <tr>
                <td width="70%">
                    ${title}
                </td>
                % if grp_model:
                <td>
                    <a id="add_groups" class="button-a" href="javascript: void(0)">${_("Add")}</a>
                    <script type="text/javascript">
                        jQuery('#add_groups').click(function() {
                            openobject.tools.openWindow(
                                openobject.http.getURL('/openerp/search/new',
                                {
                                    'model': '${grp_model}',
                                    'domain': '${grp_domain}',
                                    'context': '${grp_context}',
                                    'source': 'None',
                                    'kind': 2,
                                    'text': '',
                                    'return_to': 'True'                                    
                                })
                            );
                        });
                    </script>
                </td>
                % endif
            </tr>
        </table>
    </dt>
    % endif
    <dd>
        <ul class="ul_calGroups">
            <input type="hidden" id="_terp_colors" value="${colors}"/>
            <input type="hidden" id="groups_id" value="${[y[1] for x, y in colors.items() if y[1]]}"/>
            % for x, color in colors.items():
                <li>
                    <input type="checkbox" class="checkbox" onclick="getCalendar()" value="${color[1]}" id="${color[0]}"
                    ${py.checker(color[1] in color_values)}/>
                    <label for="${color[0]}">
                       <a href="javascript: void(0)" style="color: ${color[-1]};">${color[0]}</a>
                    </label>
                </li>
            % endfor
        </ul>
    </dd>
</dl>

