<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${_("Image")}</title>
    <script type="text/javascript">
        function do_delete(form, id, field){
            setNodeAttribute(form, 'action', openobject.http.getURL('/openerp/image/delete', {id: id}));
            jQuery('#'+form).submit();
        }

        function do_save(form, id){
            setNodeAttribute(form, 'action', openobject.http.getURL('/openerp/image/save_as', {id: id}));
            jQuery('#'+form).submit();
        }

        jQuery(document).ready(function(){
            var saved = openobject.dom.get('saved').value;
            var img = window.opener.document.getElementById('${field}');
            if(saved != '' && !parseInt(saved, 10)) {
                img.src = "data:image/png;base64," + document.getElementById('value').value;
                jQuery('input[id=${field}][type="hidden"][is_image]', window.opener.document).val(document.getElementById('value').value);
            }
            else{
                img.src = img.src + '&' + Math.random();
            }
            if(saved)
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
                        <td width="100%"><h1>${_("Image")}</h1></td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <form id="add_image" action="/openerp/image/add" method="post" enctype="multipart/form-data">
                        <input type="hidden" name="model" value="${model}"/>
                        <input type="hidden" name="id" value="${id}"/>
                        <input type="hidden" name="field" value="${field}"/>
                        <input type="hidden" id="saved" name="saved" value="${saved}"/>
                        <input type="hidden" id="value" name="value" value="${value}"/>
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
                                <a href="javascript: void(0)" class="button-a" onclick="do_save('add_image', '${id}')">${_("Save As")}</a>
                                <a href="javascript: void(0)" class="button-a" onclick="do_delete('add_image', '${id}', '${field}')">${_("Delete")}</a>
                                </td>
                                <td>
                                	<a href="javascript: void(0)" class="button-a" onclick="window.close()">${_("Close")}</a>
                                </td>
                            </tr>
                        </table>
                    </div>
                </form>
            </td>
        </tr>
    </table>
</%def>
