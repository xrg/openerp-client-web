<textarea id="${name}" name="${name}"class="${css_class}" style="width: 100%;"
    ${py.attrs(attrs, kind=kind)}>${value}</textarea>
% if editable and error:
<span class="fielderror">${error}</span>
% endif

<script type="text/javascript">
    $('#${name}').ckeditor(function(){
        this.readOnly(${int(readonly)});
    },
    {
    % if readonly:
        toolbarStartupExpanded : false
    % endif
    });
</script>
