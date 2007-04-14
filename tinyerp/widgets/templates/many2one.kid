<table width="100%" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td width="100%">
            <input type="hidden" id='${name}_domain' value="${str(domain)}"/>
            <input type="hidden" id='${name}_context' value="${str(context)}"/>
            
            <script language="javascript">
                function ${name.replace('/', '_')}_onchange(sender) {
                
                    if (sender.value == '')
                        $('${name}_value').value='';

                    onchange = "${onchange}";
                                        
                    if (!onchange) return;
                    
                    form = $("view_form");
                    
                    vals = {};
                    forEach(form.elements, function(e){
                        if (e.name &amp;&amp; e.name.indexOf('_terp_') == -1) {
                            if (e.type != 'button'){
                                vals['_terp_view_form/' + e.name] = e.value;
                            }
                        }
                    });
                    
                    vals['_terp_caller'] = '${name}';
                    vals['_terp_callback'] = onchange;
                    vals['_terp_model'] = '${model}';
                    
                    req = doSimpleXMLHttpRequest(getURL('/form/on_change', vals));
                    
                    req.addCallback(function(xmlHttp){
                        res = evalJSONRequest(xmlHttp);
                        
                        prefix = res['prefix'];
                        values = res['value'];
                        
                        //TODO: using prefix and values set value of all the fields                        
                    });                                                                                    
                }
            </script>
            
            <input type="hidden" id='${name}_value' name='${name}' value="${value or None}" py:attrs='attrs'/>
            <input style="width: 100%" type="text" id ='${name}' value="${text}" class="${field_class}" onchange="${name.replace('/', '_')}_onchange(this);" py:attrs='attrs'/>
            <br py:if="error"/><span class="fielderror" py:if="error" py:content="error"/>
        </td>
        <td>
            <div class="spacer" />
        </td>
        <td>
            <button type="button" onclick="wopen(getURL('/many2one/new', {model: '${relation}', m2o: '${name}', domain: $('${name}_domain').value, context: $('${name}_context').value}), 'search', 800, 600)" py:attrs="attrs">Select</button>
        </td>
    </tr>
</table>
