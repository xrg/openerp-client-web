<span xmlns:py="http://purl.org/kid/ns#">
    <input type="hidden" kind="${kind}" name="${name}" id="${field_id}" value="${value}"/>
    <input type="checkbox" py:attrs="checked" onclick="$('${field_id}').value = this.checked ? 1 : '';"/>
    <span class="fielderror" py:if="error"><br/>${error}</span>
</span>
