<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" 
    py:extends="tinyerp/templates/master.kid">
<head>
    <title></title>
</head>
<body>

<div class="view">

    <div class="header">

        <div class="title">
            Title goes here...
        </div>

        <div class="spacer"></div>
                        
        <div class="toolbar">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td width="100%"></td>
                    <td>
                        <button type="button" title="Switch current view: form/list">Switch</button>
                        <button type="button" title="Launch action about this resource">Action</button>
                        <button type="button" title="Print documents">Print</button>
                    </td>
                </tr>
            </table>
        </div>

    </div>

    <div class="spacer"></div>    
    
    ${tree.display()}
    
</div>

</body>
</html>
