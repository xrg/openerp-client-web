% if string:
<fieldset>
    <legend>${string}</legend>
    ${display_member(frame)}
</fieldset>
% else:
${display_member(frame)}
% endif
