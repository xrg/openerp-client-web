<form xmlns:py="http://purl.org/kid/ns#" method="post" id="${name}" name="${name}" action="${action}" enctype="multipart/form-data">
    <span py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
    <span py:if="screen" py:replace="screen.display(value_for(screen), **params_for(screen))"/>
</form>