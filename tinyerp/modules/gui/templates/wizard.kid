<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>
        <span py:if="form" py:replace="form.screen.string"/>
    </title>
    
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />
    <script language="javascript" src="/tg_static/js/MochiKit.js"></script>
    <script language="javascript" src="/static/javascript/master.js"></script>

    <script language="javascript">
    
        function wizardAction(state) {
        
            form = $('view_form');
            
            act = '/wizard/action';
            
            if (state == 'end'){
                act = '/wizard/end';
            }
            
            if (state == 'report'){
                act = '/wizard/report';
            }
            
            form.action = act;
            form._terp_state.value = state;
            
            form.submit();
        }
    </script>
    
</head>
<body>

<div class="view">

    <div class="header">

        <div class="title">
            <span py:if="form" py:replace="form.screen.string"/>
        </div>

        <div class="spacer"></div>                      

        <div class="toolbar">
            <button py:for="state in buttons" onclick="wizardAction('${state[0]}')">${state[1]}</button>
        </div>

    </div>

    <div class="spacer"></div>    
    
    <span py:if="form" py:replace="form.display()"/>
</div>

</body>
</html>
