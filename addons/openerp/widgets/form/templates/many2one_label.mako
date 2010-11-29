<label for="${name}_text" ${ "class=help" if help else "" }>
    ${string or ''}
</label>
% if help:
    <span class="help">?</span>
% endif
:
