<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <select py:if="editable" id="${field_id}" kind="${kind}" name="${name}" style="width : 100%" class="${field_class}" py:attrs='attrs' callback="${callback}" onchange="${onchange}">
        <option value=""></option>
        <option py:for="(k, v) in options" value="${k}" py:content="v" selected="1" py:if="value == k">Selected</option>
        <option py:for="(k, v) in options" value="${k}" py:content="v" py:if="value != k">Not Selected</option>
    </select>
    <span py:if="editable and error" class="fielderror" py:content="error"/>
    <span py:if="not editable" kind="${kind}" id="${name}" value="${value}" py:content="dict(options).get(value)"/>
</span>
