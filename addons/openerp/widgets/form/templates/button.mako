<button ${py.attrs(attrs)} 
    type="button" 
    id="${name}" 
    onclick="buttonClicked('${name}', '${btype}', '${model}', '${id}', '${confirm}', '${target}');">
    <table align="center" cellspacing="0">
        <tr>
            % if icon:
            <td style="text-align: center;"><img align="center" src="${icon}" width="16" height="16"/></td>
            % endif
            % if string:
            <td width="70%">${string}</td>
            % endif
        </tr>
    </table>
</button>
