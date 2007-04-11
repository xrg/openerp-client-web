<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>Search ${form.string}</title>
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />

    <script language="javascript" src="/tg_static/js/MochiKit.js"></script>
    <script language="javascript" src="/static/javascript/master.js"></script>

    <script language="javascript">
    
        function submit_form(action){
            form = $('search_form');
            form.action = action;
            form.submit();
        }       
    </script>
    
    <script language="javascript" py:if="params.m2o">
    
        function set_values(id, text){
            parent = window.opener;
            
            text_field = parent.document.getElementById('${params.m2o}');
            value_field = parent.document.getElementsByName('${params.m2o}')[0];
            
            text_field.value = text;
            value_field.value = id;
            
            window.close();
        }
    
        function onok(){
            list = new ListView('search_list');
            boxes = list.getSelected();
            
            if (boxes.length &lt; 1) return;
            
            id = boxes[0].value;
           
            req = doSimpleXMLHttpRequest(getURL('/many2one/get_string', {model: '${params.model}', id : id}));
            
            req.addCallback(function(xmlHttp){
                res = evalJSONRequest(xmlHttp);             
                set_values(id, res['name']);
            });
                                    
            return true; 
        }
                
    </script>
    
    <script language="javascript" py:if="params.m2m">
        function onok(){
        }
    </script>
    
</head>

<body>
    <div class="view">
        <div class="header">
            <div class="title">Search ${form.string}</div>
    		<div class="spacer"></div>
	    </div>

  		${form.display()}
  	</div>   	
</body>
</html>
