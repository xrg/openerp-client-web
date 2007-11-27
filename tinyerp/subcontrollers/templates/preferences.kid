<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>${screen.string}</title>
</head>
<body>
    <div class="view">        
    	<form action="/pref/ok" method="post">
            <input type="hidden" id="_terp_default" name="_terp_default" value="${ustr(defaults)}"/>
            <div class="box2 welcome">${screen.string}</div>
    	    <div class="box2" py:content="screen.display()">Screen View</div>
    	    <div class="box2" align="right">
                <button type='button' style="width: 80px" onclick="history.back()">Cancel</button>
                <button type='submit' style="width: 80px">OK</button>
    	    </div>
    	</form>
    </div>
</body>
</html>
