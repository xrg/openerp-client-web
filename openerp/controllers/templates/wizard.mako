<%inherit file="master.mako"/>

<%def name="header()">
    <title>
        % if form:
            ${form.screen.string}
        % endif
    </title>

    <script type="text/javascript" src="/static/javascript/waitbox.js"></script>
    <script type="text/javascript" src="/static/javascript/wizard.js"></script>

    <link rel="stylesheet" type="text/css" href="/static/css/waitbox.css"/>
</%def>

<%def name="content()">
<div class="view">

% if form:
    <div class="title">
    ${form.screen.string}
    </div>
% endif

    % if form:
        ${form.display()}
    % endif
    
    <div class="spacer"></div>
    
    <div class="toolbar" style="text-align: right;">
        % for state in buttons:
        <button onclick="wizardAction('${state[0]}')">${state[1]}</button>
        % endfor
    </div>
    
</div>
</%def>
