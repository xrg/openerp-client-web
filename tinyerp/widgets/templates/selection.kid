<span xmlns:py="http://purl.org/kid/ns#">
    <select id="${field_id}" name="${name}" style = "width : 100%" class="${field_class}">
        <option value=""></option>
        <option py:for="(key, value) in options" value = "${key}" py:content="value" selected="1" py:if="value == key">Selected</option>
        <option py:for="(key, value) in options" value = "${key}" py:content="value" py:if="value != key">Not Selected</option>
    </select>
    <br py:if="error"/><span class="fielderror" py:if="error" py:content="error"/>
</span>
