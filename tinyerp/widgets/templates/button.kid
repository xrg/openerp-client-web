<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <button py:if="editable" type="button" id="${name}" name="${name}" py:attrs="attrs" onclick="buttonClicked('${name}', '${btype}', '${model}', '${id}', '${confirm}');">
        <table align="center" cellspacing="0">
            <tr>
                <td py:if="icon"><img align="left" src="${icon}" width="16" height="16"/></td>
                <td py:content="string">Button Label</td>
            </tr>
        </table>
    </button>
    <button py:if="not editable" type="button" disabled="disabled">   
        <table align="center" cellspacing="0">
            <tr>
                <td py:if="icon"><img align="left" src="${icon}" width="16" height="16"/></td>
                <td py:content="string">Button Label</td>
            </tr>
        </table>
   </button> 
</span>
