<%
# put in try block to prevent improper redirection on connection refuse error
try:
    ROOT = cp.request.pool.get_controller("/openerp")
    SHORTCUTS = cp.request.pool.get_controller("/openerp/shortcuts")
    REQUESTS = cp.request.pool.get_controller("/openerp/requests")

    shortcuts = SHORTCUTS.my()
    requests, requests_message, total_mess = REQUESTS.my()
except:
    ROOT = None

    shortcuts = []
    requests = []
    requests_message = None
%>

<script type="text/javascript">
    function setRowWidth() {
        var top_divWidth = jQuery('div#top-menu').width();
        var logoWidth = jQuery('p#logo').outerWidth();

        var shortcuts = jQuery('#sc_row');
        var offset = shortcuts.outerWidth() - shortcuts.width();

        var sc_rowWidth = top_divWidth - logoWidth - offset;
        shortcuts.css('width', sc_rowWidth);
    }

    jQuery(document).ready(setRowWidth);
    jQuery(window).resize(setRowWidth);
</script>
<%
    if rpc.session.is_logged():
        logged = True
    else:
        logged = False
%>
<div id="top">
    <div id="top-menu">
        <p id="logo">
            <a href="http://www.openerp.com" target="_blank">
                <img alt="OpenERP" id="company_logo" src="/openerp/static/images/openerp_small.png"/>
            </a>
        </p>
        % if logged:
            <h1 id="title-menu">
               ${_("%(company_id)s", company_id=rpc.session.company_id or '')}
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
                    <li><a href="${py.url('/openerp/home')}" class="home">Home</a>
                        <ul>
                            <li class="first last"><a href="javascript: void(0);">Home</a></li>
                        </ul>
                    </li>

                    <li>
                        <a href="${py.url('/openerp/requests')}" class="messages">Messages<small>${total_mess}</small></a>
                        <ul>
                            <li class="first last"><a href="javascript: void(0);">Requests</a></li>
                        </ul>
                    </li>

                    <li><a href="${py.url('/openerp/pref/create')}" class="preferences">Preferences</a>
                        <ul>
                            <li class="first last"><a href="javascript: void(0);">Edit Preferences</a></li>
                        </ul>
                    </li>

                    <li><a href="javascript: void(0);" class="info">About</a>
                        <ul>
                            <li class="first last"><a href="javascript: void(0);">About</a></li>
                        </ul>
                    </li>

                    <li><a href="javascript: void(0);" class="help">Help</a>
                        <ul>
                            <li class="first last"><a href="javascript: void(0);">Help</a></li>
                        </ul>
                    </li>

                    % if cp.config('server.environment', 'openobject-web') == 'production':
                        <li id="clear_cache"><a href="${py.url('/openerp/pref/clear_cache')}" class="clear_cache">Clear Cache</a>
                            <ul>
                                <li class="first last"><a href="javascript: void(0);">Clear Cache</a></li>
                            </ul>
                        </li>
                    % endif
                </ul>
                <p class="logout"><a href="${py.url('/openerp/logout')}" target="_top">${_("Logout")}</a></p>
            </div>
        % endif
    </div>
    
    % if logged:
        <div id="shortcuts" class="menubar" cellpadding="0" cellspacing="0">
            <div id="sc_row">
                <div>
                    % for sc in shortcuts:
                        <span>
                            <a id="shortcut_${sc['res_id']}"
                               href="${py.url('/openerp/tree/open', id=sc['res_id'], model='ir.ui.menu')}">${sc['name']}</a>
                        </span>
                    % endfor
                </div>
            </div>
        </div>
    % endif
</div>
