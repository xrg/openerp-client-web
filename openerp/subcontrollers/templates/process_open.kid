<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>${form.screen.string}</title>

    <script type="text/javascript">
        var form_controller = '/process/resource';
    </script>

    <script type="text/javascript">

        MochiKit.DOM.addLoadEvent(function(evt){

            var id = parseInt($('_terp_id').value) || 0;
            var lc = $('_terp_load_counter').value;

            lc = parseInt(lc) || 1;

            if (lc > 1) {    
    
                if (id != 0) {
                    window.opener.setTimeout("window.location.reload()", 0.1);
                }
                
                return window.close();
            }
        });
    </script>

</head>
<body>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <input type="hidden" id="_terp_load_counter" value="${params.load_counter or 0}"/>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%" py:content="form.screen.string">Form Title</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td py:content="form.display()">Form View</td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="100%">
                            </td>
                            <td>
                                <button type="button" onclick="window.close()">Close</button>
                                <button type="button" onclick="submit_form('save')">Save</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>

</body>
</html>

