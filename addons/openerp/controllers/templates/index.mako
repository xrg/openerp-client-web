<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>OpenERP</title>

    <script type="text/javascript" src="/openerp/static/javascript/accordion.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/treegrid.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/notebook/notebook.js"></script>
    
    <script type="text/javascript">
        var DOCUMENT_TO_LOAD = "${load_content|n}";
        var CAL_INSTANCE = null;

        jQuery(document).ready(function () {
            jQuery('.web_dashboard').hover(function () {
                var $dashboard_item = jQuery(this);
                if(!$dashboard_item.find('img.hover')) {
                    return;
                }
                $dashboard_item.find('img').toggle();
            });

            // Don't load doc if there is a hash-url, it takes precedence
            if(DOCUMENT_TO_LOAD && !hashUrl()) {
                openLink(DOCUMENT_TO_LOAD);
                return
            }

            // Make user home widgets deletable
            jQuery('#user_widgets a.close').click(function() {
                var $widget = jQuery(this);
                jQuery.post(
                    $widget.attr('href'),
                    {widget_id: $widget.attr('id')},
                    function(obj) {
                        if(obj.error) {
                            error_display(obj.error);
                            return;
                        }
                        var $root = $widget.closest('.sideheader-a');
                        $root.next()
                             .add($root)
                             .remove();
                    }, 'json');
            });
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
            % if tools is not None:
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
                                                <li class="web_dashboard" id="${parent['id']}">
                                                    <span class="wrap">
                                                        <a href="${py.url('/openerp/menu', active=parent['id'])}" target="_top">
                                                            <table width="100%" height="100%" cellspacing="0" cellpadding="1">
                                                                <tr>
                                                                    <td align="center" style="height: 100px;">
                                                                        % if parent['web_icon_data']:
                                                                            <img src="data:image/png;base64,${parent['web_icon_data']}" alt=""/>
                                                                        % endif
                                                                        %if parent['web_icon_hover_data']:
                                                                            <img class="hover" src="data:image/png;base64,${parent['web_icon_hover_data']}" alt=""/>
                                                                        % endif
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td>
                                                                        <span>
                                                                            <strong>${parent['name']}</strong>
                                                                        </span>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </a>
                                                    </span>
                                                </li>
                                            % endfor
                                        </ul>
                                    </div>
                                </td>
                                <td class="tertiary">
                                    % if maintenance['status'] == 'none':
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
                                    % endif
                                    <div class="sideheader-a">
                                        <a href="${py.url('/openerp/widgets/add')}"
                                           id="add_user_widget" class="button-a"
                                                style="right: 1px;">${_("Add")}</a>
                                        <h2>${_("Widgets")}</h2>
                                    </div>
                                    <div class="box-a" id="user_widgets">
                                        % for widget in widgets:
                                            <div class="sideheader-a" style="padding: 0">
                                                % if widget['removable']:
                                                    <a id="${widget['user_widget_id']}"
                                                       href="${py.url('/openerp/widgets/remove')}"
                                                       class="close">${_("Close")}</a>
                                                % endif
                                                <h3>${widget['title']}</h3>
                                            </div>
                                            <div class="clean-a">
                                                ${widget['content']|n}
                                            </div>
                                        % endfor
                                    </div>
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

