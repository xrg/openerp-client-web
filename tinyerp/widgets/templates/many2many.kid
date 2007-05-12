<table xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td width="100%">
        	<script type="text/javascript">
                function ${name.replace('/', '_')}_changed(relation, listview, e, name)
                {

                    req = doSimpleXMLHttpRequest(getURL('/many2many/get_list', {model: relation, ids : e.value, list_id : name}));
                    req.addCallback(function(xmlHttp)
                    {
                        res = xmlHttp.responseText;
                        $(listview).innerHTML = res;
                        new ListView(name).checkAll();
                    });
                }
            </script>
            <input type="hidden" kind="${kind}" id='${list_view.name}_id' value="" onchange="${onchange};${name.replace('/', '_')}_changed('${relation}', '${list_view.name}_container', this, '${list_view.name}');" py:attrs='attrs' callback="${callback}"/>
            <input type="text" class="${field_class}" readonly="0" style="width: 100%" id='${list_view.name}_set' onchange="new ListView('${list_view.name}').checkAll();" py:attrs='attrs' />
            <span class="fielderror" py:if="error" py:content="error"/>
        </td>
        <td><div class="spacer"></div></td>
        <td>
            <button type="button" py:attrs='attrs' domain="${ustr(domain)}" context="${ustr(context)}" onclick="wopen(getURL('/many2many/new', {model: '${relation}', m2m: '${name}', domain: getNodeAttribute(this, 'domain'), context: getNodeAttribute(this, 'context')}), 'search', 800, 600);">
		        <table align="center">
		            <tr>
		                <td>Select</td>
		            </tr>
		        </table>
            </button>
        </td>
    </tr>
    <tr><td height="3px"></td></tr>
    <tr>
        <td colspan="3" id="${list_view.name}_container">
            ${list_view.display()}
        </td>
    </tr>
    <script language="javascript">
        new ListView('${list_view.name}').checkAll();
    </script>
</table>
