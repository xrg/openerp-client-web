<span xmlns:py="http://purl.org/kid/ns#">
    <input type="hidden" kind="${kind}" name="${name}" id="${field_id}" value="${value}"/>
    <input type="checkbox" checked="${(value or None) and 1}" onclick="$('${field_id}').value = this.checked ? 1 : '';"/>
    <span class="fielderror" py:if="error"><br/>${error}</span>
</span>
