<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <input py:if="editable" type="${invisible and 'password' or 'text'}" kind="${kind}" name='${name}' id='${field_id}' value="${value}" maxlength="${size}" class="${field_class}" py:attrs="attrs" callback="${callback}" onchange="${onchange}"/>
    <span py:if="editable and error" class="fielderror" py:content="error"/>
    <span py:if="not editable and not invisible" py:content="value"/>
    <span py:if="not editable and invisible and value" py:content="'*' * len(value)"/>
</span>
