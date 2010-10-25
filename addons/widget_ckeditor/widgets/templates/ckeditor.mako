<textarea id="${name}" name="${name}"class="${css_class}" style="width: 100%;"
    ${py.attrs(attrs, kind=kind)}>${value}</textarea>
% if editable and error:
<span class="fielderror">${error}</span>
% endif

<script type="text/javascript">
	window.onload = function()
	{
		CKEDITOR.replace( '${name}' );
	}
</script>