<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${_("Image")}</title>
    <script type="text/javascript">

        function do_delete(form, id, field){
            setNodeAttribute(form, 'action', openobject.http.getURL('/openerp/image/delete', {id: id}));
            form.submit();
        }

        function do_save(form, id){
            setNodeAttribute(form, 'action', openobject.http.getURL('/openerp/image/save_as', {id: id}));
            form.submit();
        }

        addLoadEvent(function(evt){
            img = window.opener.document.getElementById('${field}');
            img.src = img.src + '&' + Math.random();
            if(openobject.dom.get('saved').value)
                window.close();
        });

    </script>
</%def>

<%def name="content()">
    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/openerp/static/images/stock/gtk-edit.png"/>
                        </td>
                        <td width="100%">${_("Image")}</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <form action="/openerp/image/add" method="post" enctype="multipart/form-data">
                        <input type="hidden" name="model" value="${model}"/>
                        <input type="hidden" name="id" value="${id}"/>
                        <input type="hidden" name="field" value="${field}"/>
                        <input type="hidden" id="saved" name="saved" value="${saved}"/>
                        <div class="toolbar">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
                                <td class="label">${_("Add Resource:")}</td>
                                <td width="100%"><input type="file" id="upimage" name="upimage"/></td>
                            </tr>
                        </table>
                    </div>
                    <div class="spacer"></div>
                    <div class="toolbar">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
                                <td width="100%">
                                <button type="submit">${_("Save")}</button>
                                <button type="button" onclick="do_save(form, id)">${_("Save As")}</button>
                                <button type="button" onclick="do_delete(form, id, field)">${_("Delete")}</button>
                                </td>
                                <td>
                                    <button type="button" onclick="window.close()">${_("Close")}</button>
                                </td>
                            </tr>
                        </table>
                    </div>
                </form>
            </td>
        </tr>
    </table>
</%def>
