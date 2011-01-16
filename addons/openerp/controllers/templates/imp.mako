<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>Import Data</title>

    <link rel="stylesheet" type="text/css" href="/openerp/static/css/impex.css"/>
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/database.css"/>

    <script type="text/javascript">

        function do_import(form){
            if (document.getElementById('record').innerHTML){
                document.getElementById('record').innerHTML = " "
            }


            jQuery('#'+form).attr({
                'target': "detector",
                'action': openobject.http.getURL('/openerp/impex/import_data')
            }).submit();
        }

        function on_detector(src){

            jQuery('#error').dialog({
                modal: true,
                resizable: false,
                height: 150,
                width: 'auto',
                close: function(ev, ui) { $(this).remove(); }
            });

        }

        function do_autodetect(form){
            if (document.getElementById('record').innerHTML){
                document.getElementById('record').innerHTML = " "
            }

            if (! openobject.dom.get('csvfile').value ){
                return error_display(_('You must select an import file first.'));
            }

            jQuery('#'+form).attr({
                'target': "detector",
                'action': openobject.http.getURL('/openerp/impex/detect_data')
            }).submit();

        }

    % if error:
        jQuery(window.parent.document.body).append(
            jQuery('<div>', {'id': 'error', 'title': "${error.get('title', 'Warning')}"})
            .append(
                jQuery('<table>', {'class': 'errorbox'}).append(
                    jQuery('<tr>').append(
                        jQuery('<td>', {'width': '10%'})
                        .append(
                            jQuery('<img>', {'src': '/openerp/static/images/warning.png'})
                        )
                        .css('padding','4px 2px'),
                        jQuery('<td>', {'class': 'error_message_content'}).append(
                            jQuery('<pre>').html("${error.get('message', '')}")
                        )
                    ),
                    jQuery('<tr>').append(
                        '<td style="padding: 0 8px 5px 0; vertical-align:top;" align="right" colspan="2"><a class="button-a" id="error_btn" onclick="jQuery(\'#error\').dialog(\'close\');">OK</a></td>'
                    )
                )
            )
            .css('display', 'none')
        )
    % endif


    % if records:
        var $rec = jQuery('\
            <table width="100%">\
                <tr>\
                    <td width="100%" valign="middle" for="" class=" item-separator">\
                        <div class="separator horizontal">2. Check your file format</div>\
                    </td>\
                </tr>\
            </table>\
            <table id="test" class="grid" width="100%">\
                % for j, i in enumerate(records):
                    % if j == 0:
                        <tr class="grid-header">\
                            % for l, k in enumerate(i):
                              <th class="grid-cell">${i[l]}</th>\
                            % endfor
                         </tr>\
                     % else:
                         <tr class="grid-row">\
                            % for l, k in enumerate(i):
                              <td id="cell-${l}" name="cell" class="grid-cell">${i[l]}</td>\
                            % endfor
                         </tr>\
                     % endif
                % endfor
            </table>\
        ');
        jQuery(window.parent.document.getElementById('record')).append($rec);
    % endif

    </script>

</%def>

<%def name="content()">
<form name="import_data" id="import_data" action="/openerp/impex/import_data" method="post" enctype="multipart/form-data">

    <input type="hidden" id="_terp_source" name="_terp_source" value="${source}"/>
    <input type="hidden" id="_terp_model" name="_terp_model" value="${model}"/>
    <input type="hidden" id="_terp_ids" name="_terp_ids" value="[]"/>
    <input type="hidden" id="_terp_fields2" name="_terp_fields2" value="[]"/>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td class="side_spacing">
                <table width="100%" class="popup_header">
                    <tr>
                        <td align="center" class="pop_head_font">${_("Import Data")}</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
                <table width="100%">
                    <tr>
                        <td width="100%" valign="middle" for="" class=" item-separator" colspan="4">
                            <div class="separator horizontal">1. Import a .CSV file</div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            Select a .CSV file to import. If you need a sample of file to import,
                            you should use the <a style="color: blue;" href="javascript: void(0)" onclick="window.location.href=openobject.http.getURL('/openerp/impex/exp',{_terp_model: '${model}', _terp_source: '${source}'})">export tool</a> with the "Import Compatible" option.
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
                <table align="center">
                    <tr>
                        <td class="label"><label for="csvfile">${_("CSV File:")}</label></td>
                        <td>
                            <input type="file" id="csvfile" size="50" name="csvfile" onchange="do_autodetect('import_data')"/>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td height="10px">
            </td>
        </tr>
        <tr>
            <td class="side_spacing" width="100%">
                <div id="record"></div>
            </td>
        </tr>
        <tr>
            <td height="10px">
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
                <fieldset>
                    <legend>${_("CSV Options")}</legend>
                    <table>
                        <tr>
                            <td class="label"><label for="csv_separator">${_("Separator:")}</label></td>
                            <td><input type="text" name="csvsep" id="csv_separator" value=","/></td>
                            <td class="label"><label for="csv_delimiter">${_("Delimiter:")}</label></td>
                            <td><input type="text" name="csvdel" id="csv_delimiter" value='"'/></td>
                        </tr>
                        <tr>
                            <td class="label"><label for="csv_encoding">${_("Encoding:")}</label></td>
                            <td>
                                <select name="csvcode" id="csv_encoding">
                                    <option value="utf-8">UTF-8</option>
                                    <option value="latin1">Latin 1</option>
                                </select>
                            </td>
                            <td class="label"><label for="csv_skip">${_("Lines to skip:")}</label></td>
                            <td><input type="text" name="csvskip" id="csv_skip" value="1"/></td>
                        </tr>
                    </table>
                </fieldset>
            </td>
        </tr>
        <tr>
            <td height="20px">
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
                <table width="100%">
                    <tr>
                        <td class="imp-header" align="right">
                            <a class="button-a" href="javascript: void(0)" onclick="window.frameElement.close()">${_("Close")}</a>
                            <a class="button-a" href="javascript: void(0)" onclick="do_import('import_data');">${_("Import File")}</a>
                        </td>
                        <td width="5%"></td>
                </table>
            </td>
        </tr>
    </table>
</form>

<iframe name="detector" id="detector" style="display: none;" src="about:blank" onload="on_detector(this)"></iframe>
</%def>
