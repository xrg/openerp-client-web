<%! show_header_footer = False %>
<%inherit file="master.mako"/>

<%def name="header()">
    <title>Save as a Shortcut</title>
</%def>

<%def name="content()">
	<form name="filter_sc" method="POST" action="/search/do_filter_sc">
		<input type="hidden" id="search_view_id" name="search_view_id" value="${search_view_id}"/>
		<input type="hidden" id="model" name="model" value="${model}"/>
		<input type="hidden" id="domain" name="domain" value="${domain}"/>
		<input type="hidden" id="flag" name="flag" value="${flag}"/>
		
		<table class="view" width="100%" border="0">
			<tr>
	            <td width="100%" colspan="2">
	                <table class="titlebar">
	                    <tr>
	                        <td width="32px" align="left">
	                            <img src="/static/images/stock/gtk-index.png"/>
	                        </td>
	                        <td align="center" width="100%">${_("Save as a Shortcut")}</td>
	                    </tr>
	                </table>
	            </td>
	        </tr>
	        <tr>
	        	<td class="label">
	        		Shortcut Name :
	        	</td>
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
	                            <td><button type="submit" onclick="window.close()">${_("Ok")}</button></td>
	                            <td><button type="button" onclick="window.close()">${_("Close")}</button></td>
	                        </tr>
	                    </table>
	        		</div>
	        	</td>
	        </tr>
		</table>
	</form>
</%def>