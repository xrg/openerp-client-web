<%
# put in try block to prevent improper redirection on connection refuse error
try:
    ROOT = cp.request.pool.get_controller("/openerp")
    SHORTCUTS = cp.request.pool.get_controller("/openerp/shortcuts")
    REQUESTS = cp.request.pool.get_controller("/openerp/requests")

    shortcuts = SHORTCUTS.my()
    requests, total_request = REQUESTS.my()
except:
    ROOT = None

    shortcuts = []
    requests = []
    requests_message = None

if rpc.session.is_logged():
    logged = True
else:
    logged = False
%>
<td id="top" colspan="3">
    <p id="cmp_logo">
        <a href="/" target="_top">
            <img alt="OpenERP" id="company_logo" src="/openerp/static/images/openerp_small.png"/>
        </a>
    </p>
    % if logged:
        <h1 id="title-menu">
           ${_("%(company)s", company=rpc.session.company_name or '')} (${rpc.session.db})
           <small>${_("%(user)s", user=rpc.session.user_name)}</small>
        </h1>
    % endif
    <ul id="skip-links">
        <li><a href="#nav" accesskey="n">Skip to navigation [n]</a></li>
        <li><a href="#content" accesskey="c">Skip to content [c]</a></li>
        <li><a href="#footer" accesskey="f">Skip to footer [f]</a></li>
    </ul>
    % if logged:
        <div id="corner">
            <ul class="tools">
                <li><a href="${py.url('/openerp')}" target="_top" class="home">${_("Home")}</a>
                    <ul>
                        <li class="first last"><a href="${py.url('/openerp')}" target="_top">${_("Home")}</a></li>
                    </ul>
                </li>
                <li>
                    <a href="${py.url('/openerp/requests')}" class="req_messages"><small>${total_request}</small></a>
                    <ul>
                        <li class="first last"><a href="${py.url('/openerp/requests')}">${_("Requests")}</a></li>
                    </ul>
                </li>

                <li class="preferences">
                    <a href="${py.url('/openerp/pref/create')}"
                       class="preferences" target="_blank">${_("Preferences")}</a>
                    <ul>
                        <li class="first last"><a href="${py.url('/openerp/pref/create')}"
                                                  target="_blank">${_("Edit Preferences")}</a></li>
                    </ul>
                </li>
                <li><a href="${py.url('/', next='/openerp/about')}"
                       target="_top" class="info">${_("About")}</a>
                    <ul>
                        <li class="first last"><a href="${py.url('/', next='/openerp/about')}"
                                                  target="_top">${_("About")}</a></li>
                    </ul>
                </li>

                <li><a target="_blank" href="http://doc.openerp.com/book" class="help">${_("Help")}</a>
                    <ul>
                        <li class="first last"><a target="_blank" href="http://doc.openerp.com/book">${_("Help")}</a></li>
                    </ul>
                </li>

                % if cp.config('server.environment') == 'production':
                    <li id="clear_cache"><a href="${py.url('/openerp/pref/clear_cache')}"
                                            class="clear_cache" target="_top">${_("Clear Cache")}</a>
                        <ul>
                            <li class="first last"><a href="${py.url('/openerp/pref/clear_cache')}"
                                                      target="_top">${_("Clear Cache")}</a></li>
                        </ul>
                    </li>
                % endif
            </ul>
            <p class="logout"><a href="${py.url('/openerp/logout')}" target="_top">${_("Logout")}</a></p>
        </div>
    % endif
    
    <div id="shortcuts" class="menubar">
    % if logged:
        <ul>
            % for i, sc in enumerate(shortcuts):
                <li class="${i == 0 and 'first' or ''}">
                    <a id="shortcut_${sc['res_id']}"
                       href="${py.url('/openerp/tree/open', id=sc['res_id'], model='ir.ui.menu')}">
                       <span>${sc['name']}</span>
                    </a>
                </li>
            % endfor
        </ul>
    % endif
    </div>
</td>
<script type="text/javascript">
    jQuery('.tools li.preferences a').click(function (e) {
        e.preventDefault();
        openobject.tools.openWindow(this.href);
    });

    jQuery('div#shortcuts a ').live('click', function (e) {
        e.preventDefault();
    });

</script>

