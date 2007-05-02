<span xmlns:py="http://purl.org/kid/ns#">
    <fieldset py:if="string">
        <legend py:content="string" />
        ${frame.display(value_for(frame), **params_for(frame))}
    </fieldset>
    <span py:replace="frame.display()" py:if="not string"/>
</span>
