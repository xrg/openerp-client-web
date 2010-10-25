<label for="${name}_checkbox_" ${ "class=help" if help else "" }>
    ${string or ''}
</label>
% if help:
    <sup class="help">?</sup>
% endif
:
