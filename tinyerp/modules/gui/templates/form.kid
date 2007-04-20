<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>${form.screen.string} </title>
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />

    <script language="javascript" src="/tg_static/js/MochiKit.js"></script>
    <script language="javascript" src="/static/javascript/master.js"></script>
       
</head>
<body>

<div class="view">

    <div class="header">

        <div class="title">
            ${form.screen.string}
        </div>

        <div class="spacer"></div>
                        
<?python 
but_attrs = {}
if form.screen.view_mode[0] == 'tree': but_attrs['disabled'] = 0
?>

            <div class="toolbar">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td width="100%">
                        <button type="button" title="Create a new resource" onclick="submit_form('new')">New</button>
                        <button type="button" title="Edit/Save this resource" py:attrs="but_attrs" onclick="submit_form('save')">Save</button>
                        <button type="button" title="Delete this resource" onclick="submit_form('delete')" py:attrs="but_attrs">Delete</button>
                        <button type="button" title="Go to previois matched search" py:attrs="but_attrs" onclick="submit_form('prev')">Prev</button>
                        <button type="button" title="Go to next match search" py:attrs="but_attrs" onclick="submit_form('next')">Next</button>
                        <button type="button" title="Find a resource" onclick="submit_form('find')">Find</button>
                        <button type="button" title="Switch current view: form/list" onclick="submit_form('switch')">Switch</button>
                    </td>
                    <td>
                        <button type="button" title="Launch action about this resource" onclick="submit_form('action')">Action</button>
                        <button type="button" title="Print documents" onclick="submit_form('report')">Print</button>
                    </td>
                </tr>
            </table>
        </div>

    </div>

    <div class="spacer"></div>    
    
    ${form.display()}
</div>

</body>
</html>
