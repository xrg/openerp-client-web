<div xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <div py:for="w in hiddens" style="display: none;" py:content="w.display()"/>
    <table width="100%" border="0" class='fields'>
        <tr py:for="row in table">
            <td py:for="attrs, widget  in row" py:attrs="attrs">
                <span py:if="isinstance(widget, basestring)" py:strip="">
                    <sup py:if="attrs.get('title')" style="color: darkgreen;">?</sup>${(widget or '') and widget + ' :'}
                </span>
                <span py:if="not isinstance(widget, basestring) and widget.visible" 
                    py:replace="widget.display(value_for(widget), **params_for(widget))"/>
            </td>
        </tr>
    </table>
</div>
