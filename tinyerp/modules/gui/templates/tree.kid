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

            if (action == 'switch'){
                form.target = '_blank';
            } else {
                form.target = null;
            }

            form.submit();
        }
        
    </script>
</head>
<body>

<div class="view">

    <div class="header">

        <div class="title">
            ${tree.string}
        </div>

        <div class="spacer"></div>

        <div class="toolbar">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td width="100%"></td>
                    <td>
                        <button type="button" title="Switch current view: form/list" onclick="submit_form('switch')">Switch</button>
                        <button type="button" title="Launch action about this resource" onclick="submit_form('action')">Action</button>
                        <button type="button" title="Print documents" onclick="submit_form('report')">Print</button>
                    </td>
                </tr>
            </table>
        </div>

    </div>

    <div class="spacer"></div>

    ${tree.display()}

</div>

</body>
</html>
