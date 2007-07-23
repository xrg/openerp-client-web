<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>Field Preferences</title>
</head>
<body>

<form action="/fieldpref/save" method="post">

    <input id="_terp_model" name="_terp_model" value="${model}" type="hidden"/>
    <input id="_terp_model" name="_terp_field/name" value="${field['name']}" type="hidden"/>
    <input id="_terp_model" name="_terp_field/value" value="${field['value']}" type="hidden"/>
    <input id="_terp_model" name="_terp_field/string" value="${field['string']}" type="hidden"/>
    <input id="_terp_model" name="_terp_deps2" value="${str(deps)}" type="hidden"/>
                
    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%">Field Preferences</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>

                <table border="0" width="100%">
                    <tr>
                        <td class="label">Field Name:</td>
                        <td class="item" width="100%"><input type="text" disabled="disabled" value="${field['string']}"/></td>
                    </tr>
                    <tr>
                        <td class="label">Domain:</td>
                        <td class="item"><input type="text" disabled="disabled" value="$model"/></td>
                    </tr>
                    <tr>
                        <td class="label">Default Value:</td>
                        <td class="item"><input type="text" disabled="disabled" value="${field['value']}"/></td>
                    </tr>                        
                    <tr>
                        <td colspan="2">
                            <fieldset>
                                <legend><strong>Value applicable for</strong></legend>
                                <table border="0">
                                    <tr>
                                        <td class="item"><input type="radio" class="radio" name="_terp_you" value="True" checked="checked"/></td><td>only for you</td>
                                        <td class="item"><input type="radio" class="radio"/></td><td>for all</td>                                            
                                    </tr>
                                </table>                                    
                            </fieldset>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <fieldset>
                                <legend><strong>Value applicable if</strong></legend>
                                <table border="0">
                                    <tr py:if="not deps"><td>Always applicable!</td></tr>
                                    <tr py:if="deps">
                                        <!-- <td class="item"><input type="checkbox" class="checkbox" name="deps" value="${deps['name']}"/></td><td>${deps['name']} = ${deps['value']}</td> -->
                                        <span py:for="n, n, v, v in deps" py:strip="">
                                            <td><input type="checkbox" class="checkbox" name="_terp_deps/${n}" value="${v}"/></td><td>${n} = ${v}</td>
                                        </span>
                                    </tr>
                                </table>                                    
                            </fieldset>
                        </td>
                    </tr>                        
                </table>

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
		                        <button type="button" onclick="window.close()">Close</button>
		                    </td>
                            <td>
                                <button type="submit">OK</button>
                            </td>                            
		                </tr>
		            </table>
		        </div>
            </td>
        </tr>
    </table>
</form>

</body>
</html>
