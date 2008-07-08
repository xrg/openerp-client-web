<table width="100%" border="0" class='fields' xmlns:py="http://purl.org/kid/ns#">
    <input type="hidden" py:for="w in hiddens" class="${w.field_class}" kind="${w.kind}"
	       id="${w.name}" name="${w.name}" value="${w.get_display_value()}" disabled="${w.readonly or None}" 
		   relation="${getattr(w, 'relation', None)}"/>
		   
    <tr py:for="row in table">
        <td py:for="attrs, widget  in row" py:attrs="attrs">
            <span py:if="isinstance(widget, basestring)" py:replace="(widget or '') and widget + ' :'"/>
            <span py:if="not isinstance(widget, basestring) and widget.visible" py:replace="widget.display(value_for(widget), **params_for(widget))"/>
        </td>
    </tr>
</table>
