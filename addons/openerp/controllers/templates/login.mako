<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${_("Login")}</title>
    <script type="text/javascript">
        // replace existing openLink to intercept transformations of hash-urls
        var openLink = function (url) {
            jQuery(document).ready(function () {
                var form = jQuery('#loginform');
                var separator = (form.attr('action').indexOf('?') == -1) ? '?' : '&';
                form.attr('action',
                          form.attr('action') + separator + jQuery.param({'next': url}));
            })
        }
    </script>
</%def>

<%def name="content()">
    <table width="100%">
        <tr><%include file="header.mako"/></tr>
    </table>

    <table class="view" cellpadding="0" cellspacing="0" style="padding-top: 25px; border:none;">
        <tr>
            <td style="padding:35px 10px 5px 35px; min-width:100px;" valign="top" width="450">
                <form action="${py.url(target)}" method="post" name="loginform" id="loginform" style="padding-bottom: 5px; min-width: 100px;">
                    % for key, value in origArgs.items():
                        <input type="hidden" name="${key}" value="${value}"/>
                    % endfor
                    <input name="login_action" value="login" type="hidden"/>

                    <fieldset class="box">
                        <legend style="padding: 4px;">
                            <img src="/openerp/static/images/stock/stock_person.png" alt=""/>
                        </legend>
                        <div class="box2" style="padding: 5px 5px 20px 5px">
                            <table width="100%" align="center" cellspacing="2px" cellpadding="0" style="border:none;">
                                <tr>
                                    <td class="label"><label for="db">${_("Database:")}</label></td>
                                    <td style="padding: 3px;">
                                        % if dblist is None:
                                            <input type="text" name="db" id="db" class="db_user_pass" value="${db}"/>
                                        % else:
                                            <select name="db" id="db" class="db_user_pass">
                                                % for v in dblist:
                                                    <option value="${v}" ${v==db and "selected" or ""}>${v}</option>
                                                % endfor
                                            </select>
                                        % endif
                                    </td>
                                </tr>
                                <tr>
                                    <td class="label"><label for="user">${_("User:")}</label></td>
                                    <td style="padding: 3px;"><input type="text" id="user" name="user" class="db_user_pass" value="${user}" autofocus="true"/></td>
                                </tr>
                                <tr>
                                    <td class="label"><label for="password">${_("Password:")}</label></td>
                                    <td style="padding: 3px;"><input type="password" value="${password}" id="password" name="password" class="db_user_pass"/></td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td class="db_login_buttons">
                                        % if cp.config('dbbutton.visible', 'openerp-web'):
                                            <button type="button" class="static_boxes" tabindex="-1" onclick="location.href='${py.url('/openerp/database')}'">${_("Databases")}
                                            </button>
                                        % endif
                                        <button type="submit" class="static_boxes">${_("Login")}</button>
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </fieldset>
                </form>
                % if message:
                    <div class="login_error_message" id="message">${message}</div>
                % endif

                % if info:
                    <div class="information">${info|n}</div>
                % endif
                <div style="margin-top: 10px">
                    <table cellpadding="0" cellspacing="0" width="100%" style="border:none;">
                        <tr>
                            <td style="padding-left:0;"><h3> ${_("Top Contributor:")}</h3></td>
                        </tr>
                        <tr>
                            <td style="padding-left:0;"><img src="/openerp/static/images/axelor_logo.png"/></td>
                        </tr>
                    </table>
                </div>
            </td>

            <td style="padding:55px 35px 5px 10px; min-width: 200px;" valign="top">
                <p>${_("We think that daily job activities can be more intuitive, efficient, automated, .. and even fun.")}</p>
                <h3>${_("OpenERP's vision to be:")}</h3>

                <table cellpadding="0" cellspacing="0" width="100%" style="border:none;">
                    <tr>
                        <td class="feature-image">
                            <img src="/openerp/static/images/icons/product.png"/>
                        </td>
                        <td class="feature-description">
                            <strong>${_("Full featured")}</strong><br/>
                            ${_("Today's enterprise challenges are multiple. We provide one module for each need.")}
                        </td>
                    </tr>
                    <tr>
                        <td class="feature-image">
                            <img src="/openerp/static/images/icons/accessories-archiver.png"/>
                        </td>
                        <td class="feature-description">
                            <strong>${_("Open Source")}</strong><br/>
                            ${_("To Build a great product, we rely on the knowledge of thousands of contributors.")}
                        </td>
                    </tr>
                    <tr>
                        <td class="feature-image">
                            <img src="/openerp/static/images/icons/partner.png"/>
                        </td>
                        <td class="feature-description">
                            <strong>${_("User Friendly")}</strong><br/>
                            ${_("In order to be productive, people need clean and easy to use interface.")}
                        </td>
                    </tr>
                </table>

            </td>
        </tr>
    </table>
    
    <%include file="footer.mako"/>
</%def>
