<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <input py:if="editable" type="${password and 'password' or 'text'}" kind="${kind}" name='${name}' id='${field_id}' value="${value}" maxlength="${size}" class="${field_class}" py:attrs="attrs"/>
    <span py:if="editable and error" class="fielderror" py:content="error"/>
    <span py:if="not editable and not password" kind="${kind}" id="${name}" py:content="value"/>
    <span py:if="not editable and password and value" py:content="'*' * len(value)"/>
</span>
