<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />
    <title>${title}</title>    
 </head>

<body>

    <div id="content">
        <div class="view">        
	        <div class="header">
	            <div class="title">${title}</div>
	        </div>	
	        
	        <div class="spacer"/>
	        		
		    <div class="fields">
		        <pre py:content="message"/>
		    </div>
	    </div>
    </div>

</body>

</html>
