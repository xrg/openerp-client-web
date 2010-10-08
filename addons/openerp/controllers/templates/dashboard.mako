<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>
<%def name="header()">
    <title>OpenERP Dashboard</title>

    <script type="text/javascript" src="/openerp/static/javascript/accordion.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/treegrid.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/notebook/notebook.js"></script>
</%def>
<%def name="content()">
    <div id="root">
        <table id="content" class="three-a" width="100%" height="100%">
            <tr>
                <%include file="header.mako"/>
            </tr>
            <tr>
                <td id="main_nav" colspan="3">
                    <div id="applications_menu">
                        <ul>
                            %for parent in parents:
                                <li>
                                    <a href="${py.url('/openerp/menu', active=parent['id'])}"
                                       target="_top" class="${parent.get('active', '')}">
                                        <span>${parent['name']}</span>
                                    </a>
                                </li>
                            % endfor
                        </ul>
                    </div>
                </td>
            </tr>
            <tr>
                <td id="primary" width="100%" height="100%">
                    <div class="wrap" style="padding: 10px;">
                        <ul class="sections-a">
                            %for parent in parents:
                                <li id="${parent['id']}" class="${'-'.join(parent['name'].split(' ')).lower()}">
                                    <span class="wrap">
                                        <a href="${py.url('/openerp/menu', active=parent['id'])}">
                                            <span>
                                                <strong>${parent['name']}</strong>
                                            </span>
                                        </a>
                                    </span>
                                </li>
                            % endfor
                        </ul>
                    </div>
                </td>
            </tr>
        </table>
    </div>
</%def>
