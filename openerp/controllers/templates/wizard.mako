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

    <div class="header">

        <div class="title">
            % if form:
                ${form.screen.string}
            % endif
        </div>

        <div class="spacer"></div>

        <div class="toolbar">
            % for state in buttons:
            <button onclick="wizardAction('${state[0]}')">${state[1]}</button>
            % endfor
        </div>

    </div>

    <div class="spacer"></div>

    % if form:
        ${form.display()}
    % endif
</div>
</%def>
