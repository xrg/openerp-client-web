<span xmlns:py="http://purl.org/kid/ns#">
    <input type="text" kind="${kind}" name='${name}' id ='${field_id}' style = "width : 100%" value="${value}" class="${field_class}" py:attrs='attrs'
        callback="${onchange}" onchange="${(onchange or None) and 'onChange(this);'}"/>
    <br py:if="error"/><span class="fielderror" py:if="error" py:content="error"/>
</span>
