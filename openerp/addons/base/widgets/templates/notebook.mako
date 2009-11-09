<div id="${name}">
    % for page in children:
    <div class='notebook-page' ${py.attrs(title=page.string, attrs=page.attributes, widget=fake_widget)}>
        <div>${display_member(page)}</div>
    </div>
    % endfor
</div>
<script type="text/javascript">
    new Notebook('${name}', {
        'closable': false,
        'scrollable': true
    });
</script>

