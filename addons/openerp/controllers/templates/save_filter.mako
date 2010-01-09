<%inherit file="/openobject/controllers/templates/base.mako"/>

<%def name="header()">
    <title>Save as a Shortcut</title>
    
    <script type="text/javascript">
    	
    	var onFilterClose = function(form, sc_id){
    	
			form.submit();			
			var act = openobject.http.getURL("/tree/open", {id: sc_id, model: 'ir.ui.menu'});
			
		    window.opener.location.href = act;
		    
		    window.close();
		}
		
    </script>
</%def>

<%def name="content()">
	<form name="filter_sc" method="POST" action="/search/do_filter_sc">
		<input type="hidden" id="model" name="model" value="${model}"/>
		<input type="hidden" id="domain" name="domain" value="${domain}"/>
		<input type="hidden" id="flag" name="flag" value="${flag}"/>
		<input type="hidden" id="sc_id" name="sc_id" value="${sc_id}"/>
		
		<table class="view" width="100%" border="0">
			<tr>
	            <td width="100%" colspan="2">
	                <table class="titlebar">
	                    <tr>
	                        <td width="32px" align="left">
	                            <img src="/static/images/stock/gtk-index.png"/>
	                        </td>
	                        % if flag == 'sh':
	                        	<td align="center" width="100%">${_("Save as a Shortcut")}</td>
	                        % else:
	                        	<td align="center" width="100%">${_("Save as a Filter")}</td>
	                        % endif
	                    </tr>
	                </table>
	            </td>
	        </tr>
	        <tr>
	        	% if flag == 'sh':
	        	<td class="label">
	        		Shortcut Name :
	        	</td>
	        	% else:
	        	<td class="label">
	        		Filter Name :
	        	</td>
	        	% endif
	        	<td>
	        		<input type="text" name="sc_name" style="width: 75%"/>
	        	</td>
	        </tr>
	        	<td class="label">
	        		Form View :
	        	</td>
	        	<td>
	        		<select id="form_views" name="form_views" style="width: 75%">
		    			% for val in form_views:
		                	<option value="${val[0]}">${val[1]}</option>
		                % endfor
		            </select>
	        	</td>
	        <tr>
	        	<td class="label">
	        		Tree View :
	        	</td>
	        	<td>
	        		<select id="tree_views" name="tree_views" style="width: 75%">
		    			% for val in tree_views:
		                	<option value="${val[0]}">${val[1]}</option>
		                % endfor
		            </select>
	        	</td>
	        </tr>
	        <tr>
	        	<td class="label">
	        		Graph View :
	        	</td>
	        	<td>
	        		<select id="graph_views" name="graph_views" style="width: 75%">
		    			% for val in graph_views:
		                	<option value="${val[0]}">${val[1]}</option>
		                % endfor
		            </select>
	        	</td>
	        </tr>
	        <tr>
	        	<td class="label">
	        		Calendar View :
	        	</td>
	        	<td>
	        		<select id="calendar_view" name="calendar_views" style="width: 75%">
		    			% for val in calendar_views:
		                	<option value="${val[0]}">${val[1]}</option>
		                % endfor
		            </select>
	        	</td>
	        </tr>
	        <tr>
	        	<td class="label">
	        		Gantt View :
	        	</td>
	        	<td>
	        		<select id="gantt_view" name="gantt_views" style="width: 75%">
		    			% for val in gantt_views:
		                	<option value="${val[0]}">${val[1]}</option>
		                % endfor
		            </select>
	        	</td>
	        </tr>
	        <tr>
	        	<td colspan="2" align="right">
	        		<br/>
	        		<div class="toolbar">
	        			<table border="0" cellpadding="0" cellspacing="0" width="100%">
	                        <tr>
	                            <td width="100%">&nbsp;</td>
	                            <td><button type="button" onclick="onFilterClose(form, ${sc_id});">${_("Ok")}</button></td>
	                            <td><button type="button" onclick="window.close()">${_("Close")}</button></td>
	                        </tr>
	                    </table>
	        		</div>
	        	</td>
	        </tr>
		</table>
	</form>
</%def>