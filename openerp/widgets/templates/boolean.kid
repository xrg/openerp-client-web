<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <input py:if="editable" py:attrs="attrs"
        type="hidden" 
        kind="${kind}" 
        name="${name}" 
        id="${name}" 
        value="${value}"/>
    <input py:if="editable" py:attrs="attrs" 
        type="checkbox" 
        kind="${kind}" 
        class="checkbox"
        id="${name}_checkbox_" 
        checked="${(value or None) and 1}" 
        onclick="onBooleanClicked('${name}')"/>
    <span py:if="editable and error" class="fielderror" py:content="error"/>
    <input py:if="not editable" 
        type="checkbox"
        kind="${kind}"
        class="checkbox" 
        id="${name}" 
        value="${value}" 
        checked="${(value or None) and 1}" 
        disabled="disabled"/>
</span>
