<button ${py.attrs(attrs)} 
    type="button" 
    id="${name}" 
    onclick="buttonClicked('${name}', '${btype}', '${model}', '${id}', '${confirm}', '${target}');">
    <table align="center" cellspacing="0">
        <tr>
            % if icon:
            <td><img align="left" src="${icon}" width="16" height="16"/></td>
            % endif
            % if string:
            <td>${string}</td>
            % endif
        </tr>
    </table>
</button>
