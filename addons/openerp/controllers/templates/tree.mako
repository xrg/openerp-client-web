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
                    <table cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tr>
                            % if tree.toolbar:
                                <td class="treebar" valign="top" style="padding-right: 4px">
                                    <table width="100%" cellpadding="0" cellspacing="0" class="tree-grid">
                                        <thead>
                                            <tr class="header">
                                                <th>${_("Toolbar")}</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            % for tool in tree.toolbar:
                                                <tr class="${'row_tree_toolbar' + ((tree.id == tool['id'] or '') and ' selected')}" onclick="TREEVIEW.openTree(${tool['id']}, ${tool['ids']}, this)">
                                                    <td>
                                                        <table border="0" cellpadding="0" cellspacing="0" class="tree-field">
                                                            <tr>
                                                                % if tool['icon']:
                                                                    <td>
                                                                        <img alt="" src="${tool['icon']}"
                                                                            width="32" height="32" align="left"/>
                                                                    </td>
                                                                % endif
                                                                <td>${tool['name']}</td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            % endfor
                                        </tbody>
                                    </table>
                                </td>
                            % endif
                        </tr>
                    </table>
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
