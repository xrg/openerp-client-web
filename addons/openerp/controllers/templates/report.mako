## To return report file in ajax-post request.
<html>
    <head>
    </head>
    <body>
        <form id="report" action="/openerp/report" method="POST" target="_blank">
            <input type="hidden" name="report_name" value="${name}">
            % for key, value in data.iteritems():
                <input type="hidden" name="${key}" value="${value}">
            % endfor
        </form>
        <script type="text/javascript">
            document.getElementById('report').submit();
        </script>
    </body>
</html>
