<span xmlns:py="http://purl.org/kid/ns#">
    <input type="text" name='${name}' id ='${field_id}' style="width :100%" value="${value}" class="${field_class}" py:attrs="attrs"/>
    <br py:if="error"/><span class="fielderror" py:if="error" py:content="error"/>
</span>
