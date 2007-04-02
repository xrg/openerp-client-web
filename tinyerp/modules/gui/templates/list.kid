<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>${list_view.string}</title>
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />

    <script language="javascript" src="/tg_static/js/MochiKit.js"></script>
    <script language="javascript" src="/static/javascript/master.js"></script>

    <script language="javascript">
        ${list_view.loadJS()};
    </script>

</head>
<body>

<div class="view">

    <div class="header">

        <div class="title">
            ${list_view.string}
        </div>

        <div class="spacer"></div>

        <div class="toolbar">
            <button type="button" title="Create new record..." onclick="new_record()">New</button>
            <input type="hidden" id="view_id" name="view_id" value="${view_id}"/>
            <input type="hidden" id="model" name="model" value="${model}"/>
        </div>

    </div>

    <div class="spacer"></div>
    ${list_view.display()}
</div>

</body>
</html>
