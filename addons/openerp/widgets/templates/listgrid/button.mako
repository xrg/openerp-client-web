% if visible:
    % if icon:
        <img height="16" width="16" class="listImage" src="${icon}" title="${help}" context="${ctx}" ${py.attrs(attrs)}
            onclick="new ListView('${parent_grid}').onButtonClick('${name}', '${btype}', ${id}, '${confirm}', getNodeAttribute(this, 'context'))"/>
    % else:
        <a class="button-b" href="javascript: void(0)" ${py.attrs(attrs, context=ctx)} title="${help}"
            onclick="new ListView('${parent_grid}').onButtonClick('${name}', '${btype}', ${id}, '${confirm}', getNodeAttribute(this, 'context'))">
            ${string}
        </a>
    % endif
% elif not icon:
    <span>&nbsp;</span>
% endif
