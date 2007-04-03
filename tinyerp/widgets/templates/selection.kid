<span xmlns:py="http://purl.org/kid/ns#">
    <select id="${field_id}" name="${name}" style = "width : 100%">
        <option value=""></option>
        <option py:for="(key, value) in options" value = "${key}" py:content="value" selected="1" py:if="field_value == key">Selected</option>
        <option py:for="(key, value) in options" value = "${key}" py:content="value" py:if="field_value != key">Not Selected</option>
    </select>
</span>
