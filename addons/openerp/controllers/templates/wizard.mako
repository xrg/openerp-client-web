<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
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

    <div class="toolbar wizard_toolbar" style="text-align: right;">
        % for state in buttons:
        <a class="button-b wizard_button" href="javascript: void(0)" onclick="wizardAction('${state[0]}')">
        	<table align="center" cellspacing="0">
        		<tr>
        			% if len(state) >= 3:
                    <td><img alt="" align="left" src="${state[2]}" width="16" height="16"/></td>
                    % endif
                    % if state[1]:
                    <td nowrap="nowrap">${state[1]}</td>
                    % endif
        		</tr>
        	</table>
        </a>
        % endfor
    </div>

</div>

</%def>
