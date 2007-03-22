<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:py="http://purl.org/kid/ns#" py:extends="master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Test</title>   
 </head>
 
<body>

	<div id="sidepane">
		<div class="scrollbox">
			${test_tree.display()}
		</div>
	</div>
	
	<div id="vspliter">&nbsp;</div>
	
	<div id="contentpane">	
		&nbsp;		
	</div>
</body>

</html>
