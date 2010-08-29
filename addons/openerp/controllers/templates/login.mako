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

<%include file="header.mako"/>
	<table class="view" style="padding-top: 25px;">
		<tr>
			<td width="45%" class="login-frame">
				<table>
					<tr>
						<td align="left" valign="top">
					        <form action="${py.url(target)}" method="post" name="loginform" id="loginform" style="padding-bottom: 5px;">
					            
					            % for key, value in origArgs.items():
					            	<input type="hidden" name="${key}" value="${value}"/>
					            % endfor
					            
					            <input type="hidden" name="login_action" value="login"/>
								
								<fieldset class="box">
									<legend><b style="padding: 4px;">
						            	<img src="/openerp/static/images/stock/stock_person.png"/></b>
						            </legend>
						            
						            <div class="box2">
						                <table align="center" cellspacing="2px" border="0">
						                    <tr>
						                        <td class="label"><label for="db">${_("Database:")}</label></td>
						                        <td>
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
						                        <td><input type="text" id="user" name="user" class="db_user_pass" value="${user}"/></td>
						                    </tr>
						                    <tr>
						                        <td class="label"><label for="password">${_("Password:")}</label></td>
						                        <td><input type="password" value="${password}" id="password" name="password" class="db_user_pass"/></td>
						                    </tr>
						                    <tr>
						                        <td></td>
						                        <td class="db_login_buttons">
						                            % if cp.config('dbbutton.visible', 'openobject-web'):
							                            <button type="button" class="static_boxes" tabindex="-1" onclick="location.href='${py.url('/openerp/database')}'">${_("Databases")}</button>
						                            % endif
						                            <button type="submit" class="static_boxes">${_("Login")}</button>
						                        </td>
						                    </tr>
						                </table>
						            </div>
					            </fieldset>
					        </form>
		
					        % if message:
					        	<div class="box2 message" id="message">${message}</div>
					        % endif
		
					        % if info:
					        	<div class="information">${info|n}</div>
					        % endif
					        
					        <div>
					        	<table>
					        		<tr>
							        	<td style="padding-left:0px;" ><h3> Top Contributor:</h3></td>
							        </tr>
							        <tr>
								        <td style="padding-left:0px;" ><img src="/openerp/static/images/axelor_logo.png"/></td>
					            	</tr>
					            </table>
					        </div>
						</td>
					</tr>
				</table>
			</td>
			
			<td>
				<p>We think that daily job activities can be more intuitive, efficient, automated, .. and even fun.</p>
				<p><h3>OpenERP's vision to be:</h3></p>
				
				<table>
					<tr>
						<td class="feature-image">
							<img src="/openerp/static/images/icons/product.png"/>
						</td>
					 	<td class="feature-description">
							<b>Full featured</b><br/>
							Today's enterprise challenges are multiple. We provide one module for each need.
						</td>
					</tr>
					<tr>
						<td class="feature-image">
							<img src="/openerp/static/images/icons/accessories-archiver.png"/>
						</td>
					 	<td class="feature-description">
							<b>Open Source</b><br/>
							To Build a great product, we rely on the knowledge of thousands of contributors.
						</td>
					</tr>
					<tr>
						<td class="feature-image">
							<img src="/openerp/static/images/icons/partner.png"/>
						</td>
					 	<td class="feature-description">
							<b>User Friendly</b><br/>
							In order to be productive, people need clean and easy to use interface.
						</td>
					</tr>
				</table>
				<div style="padding-top: 25px;">
					<p><h3>Latest OpenERP News</h3></p>
					<p>Working in progress...</p>
					<p>Not uploaded any news yet....</p>
				</div>
			</td>
		</tr>
	</table>
<%include file="footer.mako"/>
</%def>
