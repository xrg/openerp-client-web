<span xmlns:py="http://purl.org/kid/ns#" py:strip="">    
    <script py:if="editable" type="text/javascript">
    function open_win(site){
        var web_site;
        
        if(site.indexOf("://")== -1)
            web_site='http://'+site;
        window.open(web_site);
    }
      
    </script>
    
    <table py:if="editable" width="100%" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <input type="text" kind="${kind}" name='${name}' id ='${field_id}' style="width :100%" value="${value}" class="${field_class}" py:attrs="attrs"/>
            </td>
            <td width="2px"><div class="spacer"/></td>
            <td width="75px">
                <button type="button" onclick="open_win($('${field_id}').value);">
                    Open
                </button>
            </td>
         </tr>
     </table>
    <span py:if="editable and error" class="fielderror" py:content="error"/>
    <a py:if="editable" py:content="value" href="value"/>
</span>