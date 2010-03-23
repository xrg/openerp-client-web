<textarea id="${name}" name="${name}"class="${css_class}" style="width: 100%;"
    ${py.attrs(attrs, kind=kind)}>${value}</textarea>
% if editable and error:
<span class="fielderror">${error}</span>
% endif

<script type="text/javascript">
	window.onload = function()
	{
	    var oFCKeditor_${name} = new FCKeditor( '${name}'  ) ;
	    oFCKeditor_${name}.BasePath = "/widget_fck/static/javascript/fck_editor/" ;
	    oFCKeditor_${name}.ReplaceTextarea() ;
	}
</script>