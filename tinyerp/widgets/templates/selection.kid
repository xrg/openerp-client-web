<span xmlns:py="http://purl.org/kid/ns#" py:strip="">

    <!-- select py:if="editable" id="${field_id}" kind="${kind}" name="${name}" style="width : 100%" class="${field_class}" py:attrs='attrs' callback="${callback}" onchange="${onchange}">
        <option value=""></option>
        <option py:for="(k, v) in options" value="${k}" py:content="v" selected="1" py:if="value == k">Selected</option>
        <option py:for="(k, v) in options" value="${k}" py:content="v" py:if="value != k">Not Selected</option>
    </select -->

    <div py:if="editable" py:strip="">   
        <input type="hidden" id="${field_id}" name="${field_id}" value="${value}" class="${field_class}" kind="${kind}" py:attrs='attrs' callback="${callback}" onchange="${onchange}"/>
        <input type="text" id="__text_${field_id}" readonly="readonly" class="${field_class}" kind="${kind}"/>
        
        <div id="__selection_${field_id}" class="selection-options">
            <div class="selection-shadow">
                <a href="javascript: void(0)" class="selection-value" value="">&nbsp;</a>
                <a href="javascript: void(0)" py:for="(k, v) in options" class="selection-value" value="$k">$v</a>
            </div>
        </div>
        
        <script type="text/javascript">
            new SelectionBox('${field_id}');
        </script>
    </div>
    
    <span py:if="editable and error" class="fielderror" py:content="error"/>
    <span py:if="not editable" py:content="dict(options).get(value)"/>
</span>