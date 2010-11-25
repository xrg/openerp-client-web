<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>OpenERP</title>

    <script type="text/javascript" src="/openerp/static/javascript/accordion.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/treegrid.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/notebook/notebook.js"></script>
    
    <script type="text/javascript">
        var DOCUMENT_TO_LOAD = "${load_content}";
        var CAL_INSTANCE = null;

        jQuery(document).ready(function () {
            // Don't load doc if there is a hash-url, it takes precedence
            if(DOCUMENT_TO_LOAD && !hashUrl()) {
                openLink(DOCUMENT_TO_LOAD);
            }
        });
        
    </script>
</%def>

<%def name="content()">

    <div id="root">
        <table id="content" class="three-a open" width="100%" height="100%">
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
            % if tools:
                <tr>
                    <td id="secondary" class="sidenav-open">
                        <div class="wrap">
                            <ul id="sidenav-a" class="accordion">
                                % for tool in tools:
                                    % if tool.get('action'):
                                      <li class="accordion-title" id="${tool['id']}">
                                    % else:
                                      <li class="accordion-title">
                                    % endif
                                        <span>${tool['name']}</span>
                                    </li>
                                    <li class="accordion-content" id="content_${tool['id']}">
                                       ${tool['tree'].display()}
                                    </li>
                                % endfor
                            </ul>
                            <script type="text/javascript">
                                new Accordion("sidenav-a");
                            </script>
                        </div>
                    </td>
                    <td id="primary" width="100%" height="100%">
                        <div class="wrap">
                            <div id="appContent"></div>
                        </div>
                    </td>
                </tr>
            % else:
                <tr>
                    <td colspan="3" height="100%" valign="top">
                        <table width="100%">
                            <tr>
                                <td id="primary" width="70%">
                                    <div class="wrap" style="padding: 10px;">
                                        <ul class="sections-a">
                                            % for parent in parents:
                                                <li class="${'-'.join(parent['name'].split(' ')).lower()}">
                                                    <span class="wrap">
                                                        <a href="${py.url('/openerp/menu', active=parent['id'])}" target="_top">
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
                                <td class="tertiary">
                                    <div class="wrap" style="padding: 10px;">
                                        <ul class="split-a">
                                            <li class="one">
                                                <a class="cta-a" href="http://www.openerp.com/services/subscribe-onsite" target="_blank">
                                                    <span>
                                                        <strong>${_('Use On-Site')}</strong>
                                                        ${_("Get the OpenERP Warranty")}
                                                    </span>
                                                </a>
                                            </li>
                                            <li class="two">
                                                <a class="cta-a" href="http://www.openerp.com/online" target="_blank">
                                                    <span>
                                                        <strong>${_('Use Online')}</strong>
                                                        ${_("Subscribe and start")}
                                                    </span>
                                                </a>
                                            </li>
                                        </ul>
                                    </div>
                                    <div class="sideheader-a">
                                        <ul class="side">
                                            <li>
                                                <a class="button-a" href="${py.url('/openerp/add_user_widget')}" id="add_user_widget">${_("Add")}</a>
                                            </li>
                                        </ul>
                                        <h2>${_("Widgets")}</h2>
                                    </div>
                                    <div class="box-a" id="user_widgets">
                                        % for widget in widgets:
                                            % if widget['removable']:
                                                <ul class="side">
                                                    <li>
                                                        <a id="${widget['user_widget_id']}" class="close">${_("Close")}</a>
                                                    </li>
                                                </ul>
                                            % endif
                                            <div>
                                                <h3>${widget['title']}</h3>
                                                ${widget['content']|n}
                                            </div>
                                        % endfor
                                    </div>
                                    <script type="text/javascript">
                                        jQuery(document).ready(function(){
                                            jQuery('#user_widgets.box-a ul.side a.close').click(function(){
                                                var $widget = jQuery(this);
                                                jQuery.post(
                                                    '/openerp/close_user_widget',
                                                    {widget_id: $widget.attr('id')},
                                                    function(obj) {
                                                        if(obj.error) {
                                                            error_display(obj.error);
                                                            return;
                                                        }
                                                        $widget.closest('.side').next()
                                                                .add($widget.closest('.side'))
                                                                .remove();
                                                    }, 'json');
                                            });

                                            jQuery('#add_user_widget').click(function(){
                                                window.open(this.href);
                                                return false;
                                            });
                                        });
                                    </script>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            % endif
            <tr>
                <td id="footer_section" colspan="3">
                    % if cp.config('server.environment') == 'development':
                        <div class="footer-a">
                            <p class="one">
                                <span>${rpc.session.protocol}://${_("%(user)s", user=rpc.session.loginname)}@${rpc.session.host}:${rpc.session.port}</span>
                            </p>
                            <p class="powered">${_("Powered by %(openerp)s ",
                                                openerp="""<a target="_blank" href="http://www.openerp.com/">openerp.com</a>""")|n}</p>
                        </div>
                    % else:
                        <div class="footer-b">
                            <p class="powered">${_("Powered by %(openerp)s ",
                                                openerp="""<a target="_blank" href="http://www.openerp.com/">openerp.com</a>""")|n}</p>
                        </div>
                    % endif
                </td>
            </tr>
        </table>
    </div>
</%def>

