<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <input py:if="editable" type="text" kind="${kind}" name='${name}' id ='${field_id}' value="${value}" class="${field_class}" py:attrs='attrs'/>
    <span py:if="editable and error" class="fielderror" py:content="error"/>
    <span py:if="not editable" kind="${kind}" id="${name}" value="${value}" py:content="value"/>
</span>
