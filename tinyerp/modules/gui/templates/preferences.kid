<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>${screen.string}</title>
</head>
<body>

<div class="view">
    <div class="header">
        <div class="title">${screen.string}</div>
        <div class="spacer"></div>
    </div>
    
		<form action="/pref/ok" method="post">    		
		    <input type="hidden" name="_terp_default" value="${ustr(defaults)}"/>
		    <div class="box">
		        ${screen.display()}
		    </div>			
		    <div class="spacer"></div>    
		    <div class="box">
		        <table width="100%">
		            <td align="right">
		                <button type='button' style="width: 80px" onclick="history.back()">Cancel</button>
		                <button type='submit' style="width: 80px">OK</button>
		            </td>
		        </table>
		    </div>

		</form>				
	
</div>

</body>
</html>
