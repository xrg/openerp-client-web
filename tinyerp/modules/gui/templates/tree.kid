<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>${tree.string}</title>
    <script type="text/javascript">

        function submit_form(action){
            var form = $('tree_view');

            form.action = '/tree/' + action;
            form.method = 'post';

            form.submit();
        }

    </script>
</head>
<body>

<div class="view">

    <div class="header">
        <div class="toolbar">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td width="100%">
                        <strong>${tree.string}</strong>
                    </td>
                    <td>
                        <button type="button" title="Switch current view: form/list" onclick="submit_form('switch')">Switch</button>
                        <button type="button" title="Launch action about this resource" onclick="submit_form('action')">Action</button>
                        <button type="button" title="Print documents" onclick="submit_form('report')">Print</button>
                    </td>
                    <td align="center" valign="middle" width="16">
                        <a target="new" href="${tg.query('http://tinyerp.org/scripts/context_index.php', model=tree.model, lang=rpc.session.context.get('lang', 'en'))}"><img border="0" src="/static/images/gtk-help_16x16.png" width="16" height="16"/></a>
                    </td>                    
                </tr>
            </table>
        </div>

    </div>

    <div class="spacer"></div>

    <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td py:if="tree.toolbar" class="treebar" valign="top" style="padding-right: 4px">
                <table width="100%" border="0" cellpadding="0" cellspacing="1" class="tree-grid">
                    <thead>
                        <tr class="header">
                            <th colspan="2">Toolbar</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr py:for="tool in tree.toolbar" class="${'row' + ((tree.id == tool['id'] or '') and ' selected')}" onclick="location.href='${tg.query('/tree', id=tool['id'], model=tree.model)}'">
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
            <td valign="top" py:content="tree.display()">Tree View</td>
        </tr>
    </table>

</div>

</body>
</html>
