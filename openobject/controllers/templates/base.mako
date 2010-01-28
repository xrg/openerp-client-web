<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    
% for css in widget_css:
    ${css.display()}
% endfor

    <script type="text/javascript" src="/openobject/static/javascript/MochiKit/MochiKit.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/MochiKit/DragAndDrop.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/MochiKit/Resizable.js"></script>

    <script type="text/javascript" src="/openobject/static/javascript/MochiKit/Resizable.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/MochiKit/Sortable.js"></script>
    
    <script type="text/javascript" src="/openobject/static/javascript/Sizzle/sizzle.js"></script>
    
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.base.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.gettext.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.dom.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.http.js"></script>
    <script type="text/javascript" src="/openobject/static/javascript/openobject/openobject.tools.js"></script>
    
    <script type="text/javascript">
        window.SCRIPT_PATH = "${cp.request.app.script_name}";
        openobject.http.SCRIPT_PATH = "${cp.request.app.script_name}";
    </script>
    
% for js in widget_javascript.get('head', []):
    ${js.display()}
% endfor
 
    ${next.header()}

</head>

<body>

% for js in widget_javascript.get('bodytop', []):
    ${js.display()}
% endfor

<table id="content_container" width="100%" border="0" cellspacing="0" cellpadding="0">
	<tr>
		<td>
			${self.content()}
		</td>
	</tr>
</table>

% for js in widget_javascript.get('bodybottom', []):
    ${js.display()}
% endfor

</body>
</html>
