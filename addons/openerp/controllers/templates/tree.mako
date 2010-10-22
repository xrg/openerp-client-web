<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <script type="text/javascript" src="/openerp/static/javascript/treeview.js"></script>
    
    <script type="text/javascript">
        var RESOURCE_ID = '${rpc.session.active_id}';
    </script>
    
    % if can_shortcut:
        <script type="text/javascript">
            jQuery(document).ready(function () {
                jQuery('#shortcut_add_remove').click(toggle_shortcut);
            });
        </script>
    % endif
</%def>

<%def name="content()">
    <%
        if can_shortcut:
            if rpc.session.active_id in shortcut_ids:
                shortcut_class = "shortcut-remove"
            else:
                shortcut_class = "shortcut-add"
    %>
    <table id="treeview" class="view" width="100%" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td id="body_form_td" width="100%" valign="top">
                <h1>
                    % if can_shortcut:
                        <a id="shortcut_add_remove" href="javascript: void(0)" class="${shortcut_class}"></a>
                    % endif
                    ${tree.string}
                </h1>
                <div>
                    % if tree.toolbar:
                    <div>
                        <select id="treeview-tree-selector">
                            % for tool in tree.toolbar:
                                <option value="${tool['id']}" data-ids="${tool['ids']}">
                                    ${tool['name']}
                                </option>
                            % endfor
                        </select>
                    </div>
                    % endif
                    <table cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tr>
                            <td width="100%" valign="top" class="tree_grid">${tree.display()}</td>
                        </tr>
                    </table>
                </div>
            </td>
                % if tree.sidebar:
                    <td width="163" valign="top">${tree.sidebar.display()}</td>
                % endif
        </tr>
    </table>
    
    <script type="text/javascript">
        var TREEVIEW = new TreeView(${tree.id});
    </script>
    
</%def>
