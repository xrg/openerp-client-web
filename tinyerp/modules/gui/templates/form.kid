<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>${screen.string}</title>
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />

    <script language="javascript" src="/tg_static/js/MochiKit.js"></script>
    <script language="javascript" src="/static/javascript/master.js"></script>

    <script language="javascript">
    </script>

</head>
<body>

<div class="view">

    <form method="post" id="view_form" name="view_form" action="/form/action">
    
        <input type="hidden" name="terp_model" value="${model}"/>
        <input type="hidden" name="terp_state" value="${state}"/>
        <input type="hidden" name="terp_id" value="${str(id)}"/>
        <input type="hidden" name="terp_ids" value="${str(ids)}"/>
        <input type="hidden" name="terp_view_ids" value="${str(view_ids)}"/>
        <input type="hidden" name="terp_view_mode" value="${str(view_mode)}"/>
        <input type="hidden" name="terp_view_mode2" value="${str(view_mode)}"/>
        <input type="hidden" name="terp_domain" value="${str(domain)}"/>
        <input type="hidden" name="terp_context" value="${str(context)}"/>
    
        <div class="header">

            <div class="title">
                ${screen.string}
            </div>

            <div class="spacer"></div>

            <div class="toolbar">
                <button type="submit" name="terp_action" value="new" title="Create new record...">New</button>
                <button type="submit" name="terp_action" value="save" title="Save current record...">Save</button>
                <button type="submit" name="terp_action" value="delete" title="Remove current record..." onclick="return confirm('Do you realy want to delete this record?');">Delete</button>
                <button type="submit" name="terp_action" value="search" title="Search records...">Find</button>
            </div>

        </div>

        <div class="spacer"></div>    
        
        ${screen.display()}
        
    </form>
        
</div>

</body>
</html>

