<span xmlns:py="http://purl.org/kid/ns#">
    <textarea rows="6" kind="${kind}" name='${name}' id ='${field_id}' style = "width : 100%" class="${field_class}" py:attrs='attrs' callback="${callback}" onchange="${onchange}" py:content="value"/>
    <span class="fielderror" py:if="error" py:content="error"/>
</span>