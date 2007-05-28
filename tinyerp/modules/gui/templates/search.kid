<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>Search ${form.string}</title>

    <script type="text/javascript">

        function submit_form(action){
                    
            form = $('search_form');
            form.action = action;            
                        
            // disable fields of hidden tab
            
            var hidden_tab = getElementsByTagAndClassName('div', 'tabbertabhide', 'search_form')[0];
            var disabled = [];            
            
            disabled = disabled.concat(getElementsByTagAndClassName('input', null, hidden_tab));
            disabled = disabled.concat(getElementsByTagAndClassName('textarea', null, hidden_tab));
            disabled = disabled.concat(getElementsByTagAndClassName('select', null, hidden_tab));
                                                                       
            forEach(disabled, function(fld){
                fld.disabled = true;
            });
            
            form.submit();
        }
        
        function generate_parent_fields(){
            
            pwin = window.opener;
                                    
            if (pwin &amp;&amp; pwin.document.forms &amp;&amp; pwin.document.forms.length > 0){

                pform = pwin.document.forms[0];

                forEach(pform.elements, function(e){
                    if (e.name &amp;&amp; e.name.indexOf('_terp_') == -1) {
                        if (e.type != 'button'){
                        
                            var n = '_terp_parent_form/' + e.name;
                            var v = e.value;
                            
                            appendChildNodes('search_form', INPUT({type: 'hidden', name: n, value: v}));
                            
                            if (e.attributes['kind']){
                            
                                n = '_terp_parent_types/' + e.name;
                                v = e.attributes['kind'].value;
                                
                                appendChildNodes('search_form', INPUT({type: 'hidden', name: n, value: v}));
                            }                                                                                  
                        }
                    }
                });
            }
        }
        
        if (window.opener)
            connect(window, "onload", generate_parent_fields);
        
    </script>

    <script type="text/javascript" py:if="not (params.m2o or params.m2m)">

    	function onok(action) {
			var boxes = new ListView('search_list').getSelected();
            
            if (boxes.length &lt; 1) return;
            
			var ids = []
	        id = boxes[0].value;
	        
			$('search_form')._terp_id.value = id;

			forEach(boxes, function(b){
                if (findValue(ids, b.value) == -1) ids.push(b.value);
            });

            $('search_form')._terp_ids.value = '[' + ids + ']';
            
			submit_form(action);
    	}
    </script>

    <script type="text/javascript" py:if="params.m2o">

        function onok(){

            list = new ListView('search_list');
            boxes = list.getSelected();

            if (boxes.length &lt; 1) return;

            id = boxes[0].value;

            value_field = window.opener.document.getElementById('${params.m2o}');
            value_field.value = id;

            window.opener.setTimeout("$('${params.m2o}').onchange($('${params.m2o}'))", 0);
            window.setTimeout("window.close()", 5);
        }
    </script>

    <script type="text/javascript" py:if="params.m2m">

        function onok() {

            list_view = window.opener.document.getElementById('${params.m2m}');
                        
            list_view = new ListView(list_view);
            list_new = new ListView('search_list');

            ids = [];

            boxes = list_view.getSelected();
            forEach(boxes, function(b){
                ids.push(b.value);
            });

            boxes = list_new.getSelected();
            forEach(boxes, function(b){
                if (findValue(ids, b.value) == -1) ids.push(b.value);
            });

            list_id = $('search_form__terp_m2m').value;

            req = doSimpleXMLHttpRequest(getURL('/many2many/get_list', {model: '${params.model}', ids : '[' + ids + ']', list_id: list_id}));

            req.addCallback(function(xmlHttp) {
                res = xmlHttp.responseText;

                list_view = window.opener.document.getElementById('${params.m2m}' + '_container');
                list_view.innerHTML = res;
                c = window.opener.document.getElementById('${params.m2m}'+'_set');
                c.onchange(null);

                window.setTimeout('window.close()', 0);
            });
        }

    </script>

   	<script type="text/javascript">
   	    function check_for_popup() {
   	        if(window.opener) {
                var h = $('header');
                var f = $('footer');
                h.parentNode.removeChild(h);
                f.parentNode.removeChild(f);
            }
        }
  	</script>

</head>

<body onload="check_for_popup()">
    <div class="view">
        ${form.display()}
    </div>    
</body>
</html>
