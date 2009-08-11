<%! show_header_footer = False %>
<%inherit file="master.mako"/>

<%def name="header()">
    <title>Save as a Shortcut</title>
    
    <script type="text/javascript">
    	
    	var onFilterClose = function(form, sc_id){
    	
			form.submit();			
			var act = getURL("/tree/open", {id: sc_id, model: 'ir.ui.menu'});
			
		    window.opener.location.href = act;
		    
		    window.close();
		}
		
    </script>
</%def>

<%def name="content()">
	<form name="filter_sc" method="POST" action="/search/do_filter_sc">
		<input type="hidden" id="search_view_id" name="search_view_id" value="${search_view_id}"/>
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
	        		<input type="text" name="sc_name"/>
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