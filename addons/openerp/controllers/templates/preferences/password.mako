<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/database.css"/>
    % if changed:
        <script type="text/javascript">
            window.frameElement.close();
        </script>
    % endif
</%def>

<%def name="content()">
    % for error in errors:
        ${error}<br>
    % endfor
    ${form.display()}
</%def>
