<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>${form.screen.string} </title>
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
                                
                act = getURL(act, {_terp_one2many: o2m_name});
                                
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
                                
                act = getURL(act, {_terp_one2many: o2m_name});
                                
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
                act = getURL(act, {_terp_one2many: o2m.name});
            }
                                                
            form.action = act;
            form.submit();
        }
        
        function button_clicked(name, btype, model, id, sure){
            
            if (sure && !confirm(sure)){
                return;
            }
        
            params = {};
            
            params['_terp_button/name'] = name;
            params['_terp_button/btype'] = btype;
            params['_terp_button/model'] = model;
            params['_terp_button/id'] = id;
            
            form = $("view_form");
            form.action = getURL('/form/save', params);
            form.submit();
        }
    -->
    </script>
    
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
    
    ${form.display()}
</div>

</body>
</html>
