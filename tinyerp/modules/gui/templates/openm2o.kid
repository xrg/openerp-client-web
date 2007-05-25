<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>${form.screen.string} </title>

    <script type="text/javascript" py:if="form.screen.view_mode[0]=='form'">

    	  function onclose() {
     	  	if (document.getElementsByName("_terp_id")[0] &amp;&amp; document.getElementsByName("_terp_id")[0].value != 'False')
    	  		window.opener.document.getElementById('${params.m2o}').value = document.getElementsByName("_terp_id")[0].value;
    	  	window.opener.setTimeout("$('${params.m2o}').onchange($('${params.m2o}'))", 0);
            window.setTimeout("window.close()", 5);
    	  }

          function check_for_popup() {
   	        if(window.opener) {
                var h = $('header');
                var f = $('footer');
                h.parentNode.removeChild(h);
                f.parentNode.removeChild(f);
                var s = $('sidebar_hide');
                if(s)
                	s.parentNode.removeChild(s);

                if (document.getElementsByName("_terp_id")[0] &amp;&amp; document.getElementsByName("_terp_id")[0].value != 'False')
    	  			window.opener.document.getElementById('${params.m2o}').value = document.getElementsByName("_terp_id")[0].value;
    		  	window.opener.setTimeout("$('${params.m2o}').onchange($('${params.m2o}'))", 0);
    	    }
            connect(window, 'onload', check_for_popup);

        }
        connect(window, 'onunload', onclose);
    </script>

</head>
<body onload="check_for_popup()">

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%" py:content="form.screen.string">Form Title
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
		 <tr>
            <td>${form.display()}

            </td>

        </tr>
        <tr>
            <td>
		        <div class="toolbar">
		            <table border="0" cellpadding="0" cellspacing="0" width="100%">
		                <tr>
		                    <td width="100%">
		                    </td>
		                    <td>
		                        <button type="button" onclick="onclose();">Close</button>
		                        <button type="button" onclick="submit_value('save')">Save</button>
		                    </td>
		                </tr>
		            </table>
		        </div>
            </td>
        </tr>
    </table>

</body>
</html>
