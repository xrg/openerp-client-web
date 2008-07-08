<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>
        <span py:if="form" py:replace="form.screen.string"/>
    </title>
    
    <script type="text/javascript" src="/static/javascript/waitbox.js"></script>
	<script type="text/javascript" src="/static/javascript/wizard.js"></script>
	
    <link rel="stylesheet" type="text/css" href="/static/css/waitbox.css"/>
</head>
<body>

<div class="view">

    <div class="header">

        <div class="title">
            <span py:if="form" py:replace="form.screen.string"/>
        </div>

        <div class="spacer"></div>

        <div class="toolbar">
            <button py:for="state in buttons" onclick="wizardAction('${state[0]}')">${state[1]}</button>
        </div>

    </div>

    <div class="spacer"></div>

    <span py:if="form" py:replace="form.display()"/>
    
</div>

</body>
</html>
