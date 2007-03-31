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
    <!--
        function inline_edit(id){
            form = $('view_form');
            
            form.action = '/form/edit';
            form._terp_id.value = id;
            form.submit();
        }

        function inline_delete(id){
        
            if (!confirm('Do you realy want to delete this record?')) {
                return false;
            }
        
            form = $('view_form');
            
            form.action = '/form/delete';
            form._terp_id.value = id;
            form.submit();
        }
        
        function submit_form(action){
            form = $("view_form");
            
            if (action == 'delete' &&  !confirm('Do you realy want to delete this record?')) {
                return false;
            }
            
            form.action = '/form/' + action;          
            form.submit();
        }
    -->
    </script>
    
</head>
<body>

<div class="view">

    <form method="post" id="view_form" name="view_form" action="/form/save">
    
        <input type="hidden" name="_terp_model" value="${screen.model}"/>
        <input type="hidden" name="_terp_state" value="${screen.state}"/>
        <input type="hidden" name="_terp_id" value="${str(screen.id)}"/>
        <input type="hidden" name="_terp_view_ids" value="${str(screen.view_ids)}"/>
        <input type="hidden" name="_terp_view_mode" value="${str(screen.view_mode)}"/>
        <input type="hidden" name="_terp_view_mode2" value="${str(screen.view_mode2)}"/>
        <input type="hidden" name="_terp_domain" value="${str(screen.domain)}"/>
        <input type="hidden" name="_terp_context" value="${str(screen.context)}"/>
    
        <div class="header">

            <div class="title">
                ${screen.string}
            </div>

            <div class="spacer"></div>
                        
<?python 
but_attrs = {}
if screen.view_mode[0] == 'tree': but_attrs['disabled'] = 0
?>

            <div class="toolbar">
                <button type="button" title="Create new record..." onclick="submit_form('new')">New</button>
                <button type="button" title="Save current record..." py:attrs="but_attrs" onclick="submit_form('save')">Save</button>
                <button type="button" title="Remove current record..." onclick="submit_form('delete')" py:attrs="but_attrs">Delete</button>
                <button type="button" title="Previois records..." py:attrs="but_attrs" onclick="submit_form('prev')">Prev</button>
                <button type="button" title="Next records..." py:attrs="but_attrs" onclick="submit_form('next')">Next</button>
                <button type="button" title="Search records..." onclick="submit_form('find')">Find</button>
                <button type="button" title="Switch view..." onclick="submit_form('switch')">Switch</button>
            </div>

        </div>

        <div class="spacer"></div>    
        
        ${screen.display()}
        
    </form>
        
</div>

</body>
</html>

