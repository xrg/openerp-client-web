<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <script type="text/javascript" src="/openerp/static/javascript/treeview.js"></script>
</%def>
<%def name="content()">

<table id="treeview" class="view" width="100%" border="0" cellpadding="0" cellspacing="0">
    <tr>
        <td width="100%" valign="top">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                    <td colspan="2">
                        <table width="100%" class="titlebar">
                            <tr>
                                <td width="100%"><h1>${tree.string}</h1></td>
                                <!--td nowrap="nowrap">
                                <button type="button" title="${_('Switch current view: form/list')}" onclick="TREEVIEW.switchItem()">${_("Switch")}</button>
                                </td-->
                                <td align="center" valign="middle" width="16">
                                    <a target="new" href="${py.url('http://doc.openerp.com/index.php', model=tree.model, lang=rpc.session.context.get('lang', 'en'))}"><img border="0" src="/openerp/static/images/stock/gtk-help.png" width="16" height="16"/></a>
                                </td>
                            </tr>
                         </table>
                     </td>
                 </tr>
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
                                <tr class="${'row' + ((tree.id == tool['id'] or '') and ' selected')}" onclick="TREEVIEW.openTree(${tool['id']}, ${tool['ids']}, this)">
                                    <td>
                                        <table border="0" cellpadding="0" cellspacing="0" class="tree-field">
                                            <tr>
                                                % if tool['icon']:
                                                <td><img alt="" src="${tool['icon']}"
                                                         width="32" height="32" align="left"/></td>
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
                    <td width="100%" valign="top">${tree.display()}</td>
                 </tr>
            </table>
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
