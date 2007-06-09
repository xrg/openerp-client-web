<table xmlns:py="http://purl.org/kid/ns#" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr py:if="editable">
        <td>
            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <td>
			        	<script type="text/javascript">
			                function ${name.replace('/', '_')}_changed(relation, listview, e, name) {

			                    req = Ajax.get('/search/get_list', {model: relation, ids : e.value, list_id : name});
                                
			                    req.addCallback(function(xmlHttp){
			                        res = xmlHttp.responseText;
			                        $(listview).innerHTML = res;
			                        new ListView(name).checkAll();
			                    });
			                }
			            </script>
			            <input type="hidden" kind="${kind}" id='${list_view.name}_id' value="" onchange="${onchange};${name.replace('/', '_')}_changed('${relation}', '${list_view.name}_container', this, '${list_view.name}');" py:attrs='attrs' callback="${callback}"/>
			            <input type="text" class="${field_class}" readonly="0" id='${list_view.name}_set' onchange="new ListView('${list_view.name}').checkAll();" py:attrs='attrs' style="width: 100%;"/>
			            <span class="fielderror" py:if="error" py:content="error"/>                    
                    </td>
			        <td width="2px"><div class="spacer"/></td>
			        <td width="75px" style="padding-left: 2px;">
			            <button type="button" py:attrs='attrs' domain="${ustr(domain)}" context="${ustr(context)}" onclick="open_search_window('${relation}', getNodeAttribute(this, 'domain'), getNodeAttribute(this, 'context'), '${name}', 2);">
			                Select
			            </button>
			        </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr py:if="editable"><td colspan="${(editable or None) and 3}" height="4px"></td></tr>
    <tr>
        <td colspan="${(editable or None) and 3}" id="${list_view.name}_container">
            ${list_view.display()}
            <script type="text/javascript">
                new ListView('${list_view.name}').checkAll();
            </script>
        </td>
    </tr>
</table>
