<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <textarea py:if="editable" rows="6" kind="${kind}" name='${name}' id ='${field_id}' class="${field_class}" py:attrs='attrs' callback="${callback}" onchange="${onchange}" py:content="value or None"/>
    <span py:if="editable and error" class="fielderror" py:content="error"/>
    <span py:if="not editable and value">
        <br py:for="line in value.split('\n')">${line}</br>
    </span>
</span>
