<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <button type="button" id="${name}" py:attrs="attrs" onclick="buttonClicked('${name}', '${btype}', '${model}', '${id}', '${confirm}', '${target}');">
        <table align="center" cellspacing="0">
            <tr>
                <td py:if="icon"><img align="left" src="${icon}" width="16" height="16"/></td>
                <td py:content="string">Button Label</td>
            </tr>
        </table>
    </button>
</span>
