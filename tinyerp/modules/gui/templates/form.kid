<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>${form.screen.string}</title>
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
    ${form.display()}
</div>

</body>
</html>
