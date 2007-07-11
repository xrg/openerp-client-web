<span xmlns:py="http://purl.org/kid/ns#" py:strip="">    
    <script py:if="editable" type="text/javascript">
    function open_win(site){
        var web_site;
        
        if(site.indexOf("://")== -1)
            web_site='http://'+site;
    
        if(site.length > 0) {
            window.open(web_site); 
        }
    }
      
    </script>
    
    <table py:if="editable" width="100%" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <input type="text" kind="${kind}" name='${name}' id ='${field_id}' value="${value}" class="${field_class}" py:attrs="attrs"/>
            </td>
            <td width="16">
                <img width="16" height="16" alt="Go!" src="/static/images/stock/gtk-jump-to.png" style="cursor: pointer;" onclick="open_win($('${field_id}').value);"/>
            </td>
         </tr>
     </table>
    <span py:if="editable and error" class="fielderror" py:content="error"/>
    <a py:if="not editable" py:content="value" href="${value}"/>
</span>