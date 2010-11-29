<label for="${name}_checkbox_" ${ "class=help" if help else "" }>
    ${string or ''}
</label>
% if help:
    <span class="help">?</span>
% endif
:
