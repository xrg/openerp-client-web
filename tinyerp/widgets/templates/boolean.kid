<span xmlns:py="http://purl.org/kid/ns#">
    <input type="hidden" name="${name}" id="${field_id}" value="${field_value}"/>
    <input type="checkbox" py:attrs="checked" onclick="$('${field_id}').value = this.checked ? 1 : '';"/>
</span>
