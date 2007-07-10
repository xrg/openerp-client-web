<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Config Editor</title>
</head>

<body>
    <div class="view">
    <br/>
        <table width="100%" class="titlebar">
            <tr>
                <td width="32px" align="center">
                    <img src="/static/images/icon.gif"/>
                </td>
                <td width="100%">Config Editor</td>
            </tr>
        </table>
		<div class="box2 welcome">Tiny ERP Server</div>
		    <div py:if="not passwd or message">
		        <form name="config" action="/configure/connect" method="post">
	    		    <div class="box2" id="passwd">    		    
						<table align="center" border="0" width="100%">
							<tr>
				                <td align="right" class="label">
				                    Password :
				                </td>
				                <td>
				                    <input type="password" name="passwd" style="width: 99%;"/>
				                </td>
				            </tr>                       
						</table>
					</div>
					<div class="box2">
						<table align="center" border="0" width="100%">
		                    <tr>
				                <td></td>
				                <td align="right">
	                                <button type="button" onclick="window.location.href='/login'">Cancel</button>
	                                <button type="submit">OK</button>
			                    </td>
				            </tr>
				        </table>
				    </div>    			    
    			</form>
    			<div class="box message" id="message" py:if="message" py:content="message"/> 
			</div>
		  
		    <div py:if="passwd and not message">	
		        <form name="config" action="/configure/setconf" method="post">
			        <div class="box2" id="config">
						<table align="center" border="0" width="100%">
							<tr>
				                <td align="right" class="label">
				                    Host :
				                </td>
				                <td>
				                    <input type="text" name="host" value="${host}" style="width: 99%;"/>
				                </td>
				            </tr>
				            <tr>
					            <td align='right' class="label">
			                        Port :
				                </td>
				                <td>
				                    <input type="text" name="port" value="${port}" style="width: 99%;"/>
				                </td>			                
			                </tr>
			                <tr>
					            <td align='right' class="label">
			                        Protocol :
				                </td>
				                <td>
				                    <input type="text" name="protocol" value="${protocol}" style="width: 99%;"/>
				                </td>			                
			                </tr>
						</table>
					</div>
	
	                <div class="box2">
						<table align="center" border="0" width="100%">
		                    <tr>
				                <td></td>
				                <td align="right">
	                                <button type="button" onclick="window.location.href='/login'">Cancel</button>
	                                <button type="submit">OK</button>
			                    </td>
				            </tr>
				        </table>
				    </div>    	 
				</form>       
   	        </div>
        </div>
</body>
</html>
