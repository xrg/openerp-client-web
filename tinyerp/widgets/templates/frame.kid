<table width="100%" border="0" class='fields' xmlns:py="http://purl.org/kid/ns#">
    <tr py:for="row in table">
        <td py:for="attrs, widget  in row" py:attrs="attrs">
            <span py:if="isinstance(widget, unicode)" py:replace="widget + ' :'"/>
            <span py:if="not isinstance(widget, unicode)" py:replace="widget.display(value_for(widget), **params_for(widget))"/>
        </td>
    </tr>
</table>
