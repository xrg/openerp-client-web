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
        function inline_edit(id, o2m_name){
            form = $('view_form');
            
            act = '/form/edit';
            
            if (o2m_name) {
                n = o2m_name.replace('.', '/') + '/_terp_id';
                terp_id = document.getElementsByName(n)[0];                                
                terp_id.value = id;
                                
                act = URL(act, {_terp_one2many: o2m_name});
                                
            } else {
                form._terp_id.value = id;
            }                     
            
            form.action = act;            
            form.submit();
        }

        function inline_delete(id, o2m_name){
        
            if (!confirm('Do you realy want to delete this record?')) {
                return false;
            }
        
            form = $('view_form');
            
            act = '/form/delete';
            
            if (o2m_name) {
                n = o2m_name.replace('.', '/') + '/_terp_id';
                terp_id = document.getElementsByName(n)[0];                                
                terp_id.value = id;
                                
                act = URL(act, {_terp_one2many: o2m_name});
                                
            } else {
                form._terp_id.value = id;
            }                     
            
            form.action = act;            
            form.submit();
        }
        
        function submit_form(action, o2m){
            form = $("view_form");
            
            if (action == 'delete' &&  !confirm('Do you realy want to delete this record?')) {
                return false;
            }
            
            act = '/form/' + action;
            
            if (o2m) {
                act = URL(act, {_terp_one2many: o2m.name});
            }
                                                
            form.action = act;
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
