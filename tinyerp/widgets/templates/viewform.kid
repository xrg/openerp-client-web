<form xmlns:py="http://purl.org/kid/ns#" method="post" id="${name}" name="${name}" action="${action}" enctype="multipart/form-data">
    <span py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
    <table border="0" cellpadding="0" cellspacing="0" width="100%" py:if="screen">
        <tr>
            <td py:content="screen.display(value_for(screen), **params_for(screen))"></td>
            <td py:if="screen.hastoolbar and screen.toolbar" width="50px" valign="top" class="sidebar">
                <table width="100%" cellpadding="0" cellspacing="0" py:if="screen.toolbar.get('print')">
                    <thead>
                        <tr>
                            <th>Reports</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr py:for="item in screen.toolbar['print']" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
                            <td nowrap="">${item['string']}</td>
                        </tr>
                    </tbody>
                </table>

                <table width="100%" cellpadding="0" cellspacing="0" py:if="screen.toolbar.get('action')">
                    <thead>
                        <tr>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr py:for="item in screen.toolbar['action']" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
                            <td nowrap="">${item['string']}</td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </table>
</form>