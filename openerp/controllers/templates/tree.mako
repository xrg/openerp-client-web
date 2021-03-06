<%inherit file="master.mako"/>

<%def name="header()">
    <title>${tree.string}</title>
    <script type="text/javascript">

        function switchTree(){
        
            var selection = MochiKit.DOM.getElement('_terp_ids').value;
            
            if (!selection) {
                return alert(_('You must select at least one record.'));
            }
            
            var form = document.forms['view_tree'];
            var args = {
                '_terp_selection': '[' + selection + ']'
            }
			
			getElement('_terp_domain').value = '[]';
            setNodeAttribute(form, 'action', getURL('/tree/switch', args));
            form.method = 'post';
            form.submit();
        }

        function button_click(id){
            location.href = getURL('/tree', {
                    id : id, 
                    model : $('_terp_model').value,
                    view_id : $('_terp_view_id').value,
                    domain: $('_terp_domain').value,
                    context: $('_terp_context').value});
        }

    </script>
</%def>

<%def name="content()">
<table class="view" width="100%" border="0" cellpadding="0" cellspacing="0">
    <tr>
        <td width="100%" valign="top">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                    <td colspan="2">
                        <table width="100%" class="titlebar">
                            <tr>
                                <td width="32px" align="center">
                                    <img src="/static/images/stock/gtk-find.png"/>
                                </td>
                                <td width="100%">${tree.string}</td>
                                <td nowrap="nowrap">
                                <button type="button" title="${_('Switch current view: form/list')}" onclick="switchTree()">${_("Switch")}</button>
                                </td>
                                <td align="center" valign="middle" width="16">
                                    <a target="new" href="${py.url('http://doc.openerp.com/index.php', model=tree.model, lang=rpc.session.context.get('lang', 'en'))}"><img border="0" src="/static/images/stock/gtk-help.png" width="16" height="16"/></a>
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
                                <tr class="${'row' + ((tree.id == tool['id'] or '') and ' selected')}" onclick="button_click('${tool['id']}')">
                                    <td>
                                        <table border="0" cellpadding="0" cellspacing="0" class="tree-field">
                                            <tr>
                                                % if tool['icon']:
                                                <td><img src="${tool['icon']}" width="32" height="32" align="left"/></td>
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
</%def>
