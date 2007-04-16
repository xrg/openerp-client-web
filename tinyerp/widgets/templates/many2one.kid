<table width="100%" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td width="100%">
            <input type="hidden" id='${name}_domain' value="${str(domain)}"/>
            <input type="hidden" id='${name}_context' value="${str(context)}"/>
            
            <script language="javascript">
                function ${name.replace('/', '_')}_onchange(sender) {
                                                                        
                    var value_field = $("${name}");
                    var text_field = $("${name}_text");
                    
                    if (sender.id != text_field.id &amp;&amp; sender.value != ''){
                        ${name.replace('/', '_')}_getname(value_field);
                    }

                    onchange = "${onchange}";                                        
                    if (!onchange) 
                        return;
                    
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
                        
                        prefix = prefix ? prefix + '/' : '';
                        
                        for(var k in values){
                            fname = prefix + k;                                                                                                                
                            
                            fld = $(fname);                                                        
                            fld.value = values[k];
                            
                            if (typeof fld.onchange != 'undefined'){
                                fld.onchange(onchange);
                            }
                                                                            
                        }                        
                    });                    
                }
                
                function ${name.replace('/', '_')}_getname(sender){
               
                    var value_field = $("${name}");
                    var text_field = $("${name}_text");
                                    
                    if (sender.id == text_field.id &amp;&amp; sender.value == '') {
                        value_field.value = '';
                        ${name.replace('/', '_')}_onchange(text_field);
                    }

                    if (value_field.value){
                        req = doSimpleXMLHttpRequest(getURL('/many2one/get_name', {model: '${relation}', id : value_field.value}));
                        req.addCallback(function(xmlHttp){
                            res = evalJSONRequest(xmlHttp);
                            text_field.value = res['name'];                                        
                        });
                    }
                }
                
            </script>
            
            <input type="hidden" id='${name}' name='${name}' value="${value or None}" py:attrs='attrs' onchange="${name.replace('/', '_')}_onchange(this)"/>
            <input style="width: 100%" type="text" id ='${name}_text' value="${text}" class="${field_class}" onchange="${name.replace('/', '_')}_getname(this)" py:attrs='attrs'/>
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
