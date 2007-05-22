<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <textarea rows="6" kind="${kind}" name='${name}' id ='${field_id}' class="${field_class}" py:attrs='attrs' callback="${callback}" onchange="${onchange}" py:content="value"/>
    <span class="fielderror" py:if="error" py:content="error"/>
</span>