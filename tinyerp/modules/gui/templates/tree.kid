<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>${header}</title>
</head>
<body>

<div class="view">

    <div class="title">
        ${header}
    </div>

    <div class="spacer"></div>


    <div class="content">
        ${tree.display()}
    </div>

</div>

</body>
</html>
