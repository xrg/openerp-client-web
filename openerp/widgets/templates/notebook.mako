<div class='tabber' id="${name}">
    % for page in children:
    <div class='tabbertab' ${py.attrs(title=page.string, attrs=page.attributes, widget=fake_widget)}>
        <div>${display_member(page)}</div>
    </div>
    % endfor
</div>
<script type="text/javascript">
    tabberOptions.div = getElement('${name}');
    tabberOptions.div.tabber = new tabberObj(tabberOptions);
</script>

