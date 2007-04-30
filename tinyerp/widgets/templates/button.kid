<span xmlns:py="http://purl.org/kid/ns#">
    <button type="button" style="width: 100%" id="${name}" name="${name}" py:attrs="attrs" onclick="buttonClicked('${name}', '${btype}', '${model}', '${id}', '${confirm}');">
        <table align="center">
            <tr>
                <td py:if="icon"><img align="left" src="${icon}" width="16" height="16"/></td>
                <td>${string}</td>
            </tr>
        </table>
    </button>
</span>
