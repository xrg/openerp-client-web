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
    <!--
        function submit_form(action){
            form = $('search_form');
            form.action = '/search/' + action;
            form.submit();
        }

        function setfield(model, textid, hiddenname)
        {
        	boxes = window.document.getElementsByName('check');
        	if (boxes.length > 0)
        	{
        		for(i=0;i<=boxes.length;i++)
        		{
        			if (boxes[i].checked)
        			{
        				id = window.document.getElementsByName('check')[i].value

						function settext(xmlhttp)
        				{
				        	data = evalJSONRequest(xmlhttp);
				        	window.opener.document.getElementsByName(hiddenname)[0].value = id;
				        	window.opener.document.getElementById(textid).value = data['name'];
				        	close_form();
				        }

				        function errtext(err)
				        {
				        	alert("error" + err);
				        }

        				d=doSimpleXMLHttpRequest("/search/get_string",{'model':model, 'id':id});
        				d.addCallbacks(settext,errtext);
						break;
					}
				}
			}
        }

        function close_form()
        {
        	close();
        }
    -->
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
