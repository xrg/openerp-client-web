<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>${tree.string}</title>
    <script type="text/javascript">

        function submit_form(action, src, data, target){
            
            var selection = MochiKit.DOM.getElement('tree_ids').value;
            
            if (!selection) {
                return alert('You must select at least one record.');
            }
            
            var form = document.forms['view_tree'];
            
            var args = {
                _terp_data: data ? data : null
            };
            
            args['_terp_selection'] = '[' + selection + ']';

            setNodeAttribute(form, 'action', getURL('/tree/' + action, args));
            form.method = 'post';
            form.submit();
        }

        function button_click(id){
            location.href = getURL('/tree', {id : id, model : $('_terp_model').value, domain: $('_terp_domain').value});
        }

    </script>
</head>
<body>

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
                                <td width="100%" py:content="tree.string">Tree Title</td>
                                <td nowrap="nowrap">
                                    <button type="button" title="${_('Switch current view: form/list')}" onclick="submit_form('switch')">Switch</button>
                                </td>
                                <td align="center" valign="middle" width="16">
                                    <a target="new" href="${tg.query('http://openerp.org/scripts/context_index.php', model=tree.model, lang=rpc.session.context.get('lang', 'en'))}"><img border="0" src="/static/images/stock/gtk-help.png" width="16" height="16"/></a>
                                </td>
                            </tr>
                         </table>
                     </td>
                 </tr>
                 <tr>
                    <td py:if="tree.toolbar" class="treebar" valign="top" style="padding-right: 4px">
                        <table width="100%" cellpadding="0" cellspacing="0" class="tree-grid">
                            <thead>
                                <tr class="header">
                                    <th>Toolbar</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr py:for="tool in tree.toolbar" class="${'row' + ((tree.id == tool['id'] or '') and ' selected')}" onclick="button_click('${tool['id']}')">
                                    <td>
                                        <table border="0" cellpadding="0" cellspacing="0" class="tree-field">
                                            <tr>
                                                <td><img src="${tool['icon']}" width="32" height="32" align="left"/></td>
                                                <td>${tool['name']}</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>     
                    <td width="100%" valign="top" py:content="tree.display()">Tree View</td>          
                 </tr>
            </table>
        </td>
        <td py:if="tree.sidebar" width="163" valign="top">${tree.sidebar.display()}</td>      
    </tr>
</table>

</body>
</html>
