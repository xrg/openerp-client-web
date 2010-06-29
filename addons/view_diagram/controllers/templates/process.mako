<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${_("Process")}</title>
    <link type="text/css" rel="stylesheet" href="/view_diagram/static/css/process.css"/>

    <script src="/view_diagram/static/javascript/draw2d/wz_jsgraphics.js"></script>
    <script src="/view_diagram/static/javascript/draw2d/mootools.js"></script>
    <script src="/view_diagram/static/javascript/draw2d/moocanvas.js"></script>
    <script src="/view_diagram/static/javascript/draw2d/draw2d.js"></script>

    <script src="/view_diagram/static/javascript/process.js"></script>

    <script type="text/javascript">
        var context_help = function() {
            return window.open(openobject.http.getURL('http://doc.openerp.com/index.php', {model: 'process.process', lang:'${rpc.session.context.get('lang', 'en')}'}));
        }
    </script>
    % if selection:
    <script type="text/javascript">
        var select_workflow = function() {
            var id = parseInt(openobject.dom.get('select_workflow').value, 10) || null;
            var res_model = openobject.dom.get('res_model').value || null;
            var res_id = parseInt(openobject.dom.get('res_id').value, 10) || null;
            openLink(openobject.http.getURL("/view_diagram/process", {id: id, res_model: res_model, res_id: res_id}));
        }
    </script>
    % endif
</%def>

<%def name="content()">

<table class="view" width="100%" border="0" cellpadding="0" cellspacing="0">
	<tr>
	    <td>
		    <table width="100%">
			    <tr>
			        <td width="80%" valign="top">
			            <table width="100%" class="titlebar">
			                <tr>
			                    <td width="100%" id="process_title" style="padding-left: 0px; font-weight: bold;"></td>
			                </tr>
			            </table>
			        </td>
			    	<td width="20%" align="center" >
				    	<table>
			    			<tr>
			    				<td>
									<div>
										<a class="help-button-a" href="javascript: void(0)">
											Buy a Support Contract
											<small>By Chat / Mail / Phone</small>
										</a>
									</div>
								</td>
							</tr>
							<tr>
								<td>
									<div>
										<a class="help-button-a" href="javascript: void(0)">
											Get Books
											<small>Available in Amazon</small>
										</a>
									</div>
								</td>
							</tr>
							<tr>
								<td>
									<div>
										<a class="help-button-a" href="javascript: void(0)">
											Community Forum
											<small>Join Community Discussion</small>
										</a>
									</div>
								</td>
							</tr>
						</table>
					</td>
				</tr>
			</table>
		</td>
    </tr>
	<tr>
		<td>
			<table class="view" width="100%" border="0" cellpadding="0" cellspacing="0">
				<tr>
					<td style="font-size: 14px; font-weight: bold;">Process</td>
				</tr>
				<tr>
					<td>
					    <input type="hidden" id="res_model" value="${res_model}"/>
					    <input type="hidden" id="res_id" value="${res_id}"/>
					    <fieldset>
					        <legend><b style="padding: 4px;">${_("Select Process")}</b></legend>
					        <select id="select_workflow" name="select_workflow" style="min-width: 150px">
					            % for val, text in selection:
					            <option value="${val}" ${val==id and "selected" or ""} >${text}</option>
					            % endfor
					        </select>
					        <button class="button" type="button" onclick="select_workflow()">${_("Select")}</button>
					    </fieldset>
				    </td>
			    </tr>
		    </table>
		</td>
	</tr>
	<tr>
		<td>
			<table class="view" width="100%" border="0" cellpadding="0" cellspacing="0">
			    <tr>
			        <td align="center">
			            <input type="hidden" id="id" value="${id}"/>
			            <input type="hidden" id="res_model" value="${res_model}"/>
			            <input type="hidden" id="res_id" value="${res_id}"/>
			            <div id="process_canvas" style="margin-top: 00px"></div>
			            <script type="text/javascript">
			                var id = parseInt(openobject.dom.get('id').value, 10) || 0;
			                var res_model = openobject.dom.get('res_model').value;
			                var res_id = openobject.dom.get('res_id').value;

			                if (id) {
			                    var wkf = new openobject.process.Workflow('process_canvas');
			                    wkf.load(id, res_model, res_id);
			                }
			            </script>
			        </td>
			    </tr>
			</table>
		</td>
	</tr>
	% if fields:
    <tr>
    	<td>
    		<table>
    			<tr>
    				<td align="left" style="font-size: 14px; font-weight: bold;">Fields</td>
    			</tr>
    			<tr>
    				<td align="left">
			            <table>
						% for k, v in fields.items():
							<tr>
								<td>
									<b>${k}:</b>
								</td>
								<td>${v['string']}, ${v['type']},
								% for l, m in v.items():
									% if m and (l not in ('string','type')):
										${l},
									% endif
								% endfor
								</td>
							</tr>
						% endfor
			            </table>
					</td>
				</tr>
			</table>
    	</td>
    </tr>
    % endif
    <tr>
       <td class="dimmed-text">
           <table class="form-footer">
                <tr>
	                <td class="footer" style="text-align: right;">
	                    <a target="_blank" id="show_customize_menu" href="${py.url('/openerp/form/edit', model='process.process', id=id)}">${_("Customise")}</a><br/>
	                </td>
                </tr>
            </table>
       </td>
   </tr>
</table>
</%def>
