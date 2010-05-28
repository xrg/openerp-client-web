<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>
        % if form:
            ${form.screen.string}
        % endif
    </title>

    <script type="text/javascript" src="/openerp/static/javascript/openerp/openerp.ui.waitbox.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/wizard.js"></script>

    <link rel="stylesheet" type="text/css" href="/openerp/static/css/waitbox.css"/>
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
        <button onclick="wizardAction('${state[0]}')">
            <table align="center" cellspacing="0">
                <tr>
                    % if len(state) >= 3:
                    <td><img alt="" align="left" src="${state[2]}" width="16" height="16"/></td>
                    % endif
                    <td nowrap="nowrap">${state[1]}</td>
                </tr>
            </table>
        </button>
        % endfor
    </div>
    
</div>

</%def>
