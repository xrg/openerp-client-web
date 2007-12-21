<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <textarea py:if="editable and not inline" rows="6" kind="${kind}" name='${name}' id ='${field_id}' class="${field_class}" py:attrs='attrs' callback="${callback}" onchange="${onchange}" py:content="value or None"/>
    <input py:if="editable and inline" type="text" kind="${kind}" name='${name}' id ='${field_id}' class="${field_class}" py:attrs='attrs' callback="${callback}" onchange="${onchange}" value="${value or None}"/>
    <span py:if="editable and error" class="fielderror" py:content="error"/>
    <span py:if="not editable and value">
        <br py:for="line in value.split('\n')">${line}</br>
    </span>
</span>
