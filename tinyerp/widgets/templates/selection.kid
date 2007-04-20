<span xmlns:py="http://purl.org/kid/ns#">
    <select id="${field_id}" kind="${kind}" name="${name}" style="width : 100%" class="${field_class}" py:attrs='attrs'
        callback="${callback}" onchange="${onchange}">
        
        <option value=""></option>
        <option py:for="(k, v) in options" value="${k}" py:content="v" selected="1" py:if="value == k">Selected</option>
        <option py:for="(k, v) in options" value="${k}" py:content="v" py:if="value != k">Not Selected</option>
    </select>
    <span class="fielderror" py:if="error" py:content="error"/>
</span>
