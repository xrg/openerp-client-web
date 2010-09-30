<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>
<%def name="header()">
    <title>OpenERP Dashboard</title>
    
    <link href="/openerp/static/css/treegrid.css" rel="stylesheet" type="text/css"/>
    <link href="/openerp/static/css/notebook.css" rel="stylesheet" type="text/css"/>

    <script type="text/javascript" src="/openerp/static/javascript/accordion.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/treegrid.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/notebook/notebook.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/scroll_scut.js"></script>
</%def>
<%def name="content()">
    <div id="root">
        <table id="content" class="three-a" width="100%">
            <tr>
                <%include file="header.mako"/>
            </tr>
            <tr>
                <td id="main_nav" colspan="3">
                    <a id="scroll_left" class="scroll_right" style="float: left; padding-top: 12px;" href="javascript: void(0);">
                        <img src="/openerp/static/images/scroll_left.png" alt="">
                    </a>
                    <a id="scroll_right" class="scroll_right" style="float: right; margin-right: 0; padding: 12px 5px 0 0;" href="javascript: void(0);">
                        <img src="/openerp/static/images/scroll_right.png" alt="">
                    </a>
                    
                    <div id="nav" class="sc_menu">
                        <ul class="sc_menu">
                            %for parent in parents:
                                <li id="${parent['id']}" class="menu_tabs">
                                    <a href="${py.url('/openerp/menu', active=parent['id'])}" target="_top" class="${parent.get('active', '')}">
                                        <span>${parent['name']}</span>
                                    </a>
                                    <em>[1]</em>
                                </li>
                            % endfor
                        </ul>
                    </div>
                </td>
            </tr>
            <tr>
                <td id="primary" width="100%">
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