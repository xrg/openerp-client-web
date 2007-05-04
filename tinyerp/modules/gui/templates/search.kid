<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>Search ${form.string}</title>

    <script type="text/javascript">

        function submit_form(action){
            form = $('search_form');
            form.action = action;

            pwin = window.opener;

            if (pwin &amp;&amp; pwin.document.forms &amp;&amp; pwin.document.forms.length > 0){

                pform = pwin.document.forms[0];

                pvals = {};

                forEach(pform.elements, function(e){
                    if (e.name &amp;&amp; e.name.indexOf('_terp_') == -1) {
                        if (e.type != 'button'){
                            pvals['_terp_parent_form/' + e.name] = e.value;

                            if (e.attributes['kind']){
                                pvals['_terp_parent_types/' + e.name] = e.attributes['kind'].value;
                            }
                        }
                    }
                });

                form.action = getURL(action, pvals);
            }

            form.submit();
        }
    </script>

    <script type="text/javascript" py:if="params.m2o">

        function onok(){

            list = new ListView('search_list');
            boxes = list.getSelected();

            if (boxes.length &lt; 1) return;

            id = boxes[0].value;

            parent = window.opener;

            value_field = parent.document.getElementById('${params.m2o}');

            value_field.value = id;

            parent.setTimeout("$('${params.m2o}').onchange($('${params.m2o}'))", 0);
            window.setTimeout("window.close()", 5);
        }

    </script>

    <script type="text/javascript" py:if="params.m2m">

        function onok() {

            parent = window.opener;

            list_view = parent.document.getElementById('${params.m2m}');

            list_view = new ListView(list_view);
            list_new = new ListView('search_list');

            ids = [];

            boxes = list_view.getSelected();
            forEach(boxes, function(b){
                ids.push(b.value);
            });

            boxes = list_new.getSelected();
            forEach(boxes, function(b){
                if (ids.indexOf(b.value) == -1) ids.push(b.value);
            });

            list_id = $('search_form__terp_m2m').value;

            req = doSimpleXMLHttpRequest(getURL('/many2many/get_list', {model: '${params.model}', ids : '[' + ids + ']', list_id: list_id}));

            req.addCallback(function(xmlHttp) {
                res = xmlHttp.responseText;

                list_view = parent.document.getElementById('${params.m2m}' + '_container');
                list_view.innerHTML = res
                c = parent.document.getElementById('${params.m2m}'+'_set');
                c.onchange(null);

                window.setTimeout('window.close()', 0);
            });
        }

    </script>

</head>

<body>
    <div class="view">
        <div class="header">
            <div class="title">Search ${form.string}</div>
    		<div class="spacer"></div>
	    </div>
  		${form.display()}
  	</div>
  	<script type="text/javascript">
  	 function onload()
        {
        	if(window.opener)
        	{
        		t = document.getElementById("container");
        		t.removeChild($("header"));
        		t.removeChild($("footer"));
	       	}
        }
  	</script>
</body>
</html>
