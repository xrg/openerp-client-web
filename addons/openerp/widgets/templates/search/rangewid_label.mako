<label for="${name}/from" ${ "class=help" if help else "" }>
    ${string or ''}
</label>
% if help:
    <span class="help">?</span>
% endif
:
