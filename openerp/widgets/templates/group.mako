% if string:
<fieldset>
    <legend>${string}</legend>
    ${display_child(frame)}
</fieldset>
% else:
${display_child(frame)}
% endif
