<label for="${name}" ${ "class=help" if help else "" }>
    ${string or ''}
</label>
% if help:
    <span class="help">?</span>
% endif
:
