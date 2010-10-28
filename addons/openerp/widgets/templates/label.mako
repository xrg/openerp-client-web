<label for="${name}" ${ "class=help" if help else "" }>
    ${string or ''}
</label>
% if help:
    <sup class="help">?</sup>
% endif
:
