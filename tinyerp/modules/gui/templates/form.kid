<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>${form.string}</title>
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />

    <script language="javascript" src="/tg_static/js/MochiKit.js"></script>
    <script language="javascript" src="/static/javascript/master.js"></script>

    <script language="javascript">

        function new_record(){
            window.location.href = URL('/edit', {view_id: $('view_id').value, model: $('model').value});
        }

        function save_record() {
            document.view_form.submit();
        }

        function delete_record(){
            if (confirm("Do you yeally want to delete this record?")) {
                window.location.href = URL('/delete', {view_id: $('view_id').value, model: $('model').value, id: $('id').value});
            }
        }

        function find_records(){
            wopen(URL('/find', {model: $('model').value}), "search", 800, 600);
        }
    </script>

</head>
<body>

<div class="view">

    <div class="header">

        <div class="title">
            ${form.string}
        </div>

        <div class="spacer"></div>

        <div class="toolbar">
            <button type="button" title="Create new record..." onclick="new_record()">New</button>
            <button type="button" title="Save current record..." onclick="save_record()">Save</button>
            <button py:if="id" type="button" title="Remove current record..." onclick="delete_record()">Delete</button>
            <button type="button" title="Search records..." onclick="find_records()">Find</button>
        </div>

    </div>

    <div class="spacer"></div>

    <form method="post" id="view_form" name="view_form" action="/save">
        <input type="hidden" name="view_id" id="view_id" value="${view_id}"/>
        <input type="hidden" name="model" id="model" value="${model}"/>
        <input type="hidden" name="id" id="id" value="${id}" py:if="id"/>
        ${form.display()}
    </form>

    <div class="spacer" py:if="message"></div>

    <div py:if="message" class="box message">
        ${message}
    </div>

</div>

</body>
</html>

