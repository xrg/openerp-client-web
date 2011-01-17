<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>Import Data</title>

    <link rel="stylesheet" type="text/css" href="/openerp/static/css/impex.css"/>
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/database.css"/>

    <script type="text/javascript">
        function import_results(detection) {
            jQuery('#records_data, #error, #imported_success').empty();

            // detect_data only returns the body part of this, or something
            var $detection = jQuery('<div>'+detection+'</div>');
            var $error = $detection.find('#error');
            if($error.children().length) {
                jQuery('#error')
                        .html($error.html());
                return;
            }
            var $success = $detection.find('#imported_success');
            if($success.children().length) {
                jQuery('#imported_success')
                        .html($success.html());
                return;
            }
            jQuery('#records_data')
                    .html($detection.find('#records_data').html());
        }

        function do_import() {
            if(!jQuery('#csvfile').val()) { return; }
            jQuery('#import_data').attr({
                'action': openobject.http.getURL('/openerp/impex/import_data')
            }).ajaxSubmit({
                success: import_results
            });
        }

        function autodetect_data() {
            if(!jQuery('#csvfile').val()) { return; }
            jQuery('#import_data').attr({
                'action': openobject.http.getURL('/openerp/impex/detect_data')
            }).ajaxSubmit({
                success: import_results
            });

        }

        jQuery(document).ready(function () {
            if(!window.frameElement.set_title) { return; }
            // Set the page's title as title of the dialog
            var $header = jQuery('.pop_head_font');
            window.frameElement.set_title(
                $header.text());
            $header.closest('.side_spacing').parent().remove();

            jQuery('fieldset legend').click(function () {
                jQuery(this).next().toggle();
            });
            jQuery('#csvfile, fieldset').change(autodetect_data);
        });
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
                            <h2 class="separator horizontal">${_("1. Import a .CSV file")}</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            Select a .CSV file to import. If you need a sample of file to import,
                            you should use the export tool with the "Import Compatible" option.
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
                            <input type="file" id="csvfile" size="50" name="csvfile"/>
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
                <div id="record">
                    <table width="100%">
                        <tr>
                            <td width="100%" valign="middle" for="" class=" item-separator">
                                <h2 class="separator horizontal">${_("2. Check your file format")}</h2>
                            </td>
                        </tr>
                    </table>
                    <div id="error">
                        % if error:
                            <p style="white-space:pre-line;"
                                >${_("The import failed due to: %(message)s", message=error['message'])}</p>
                            % if 'preview' in error:
                                <p>${_("Here is a preview of the file we could not import:")}</p>
                                <pre>${error['preview']}</pre>
                            % endif
                        % endif
                    </div>
                    <table id="records_data" class="grid" width="100%" style="margin: 5px 0;">
                    % if records:
                        % for rownum, row in enumerate(records):
                            % if rownum == 0:
                                <tr class="grid-header">
                                    % for title in row:
                                      <th class="grid-cell">${title}</th>
                                    % endfor
                                 </tr>
                             % else:
                                 <tr class="grid-row">
                                    % for index, cell in enumerate(row):
                                      <td id="cell-${index}" name="cell" class="grid-cell">${cell}</td>
                                    % endfor
                                 </tr>
                             % endif
                        % endfor
                    % endif
                    </table>
                    <fieldset>
                        <legend style="cursor:pointer;">${_("CSV Options")}</legend>
                        <table style="display:none">
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
                </div>
            </td>
        </tr>
        <tr id="imported_success">
            % if success:
            <td class="side_spacing">
                <table width="100%">
                    <tr>
                        <td width="100%" valign="middle" for="" class=" item-separator" colspan="4">
                            <h2 class="separator horizontal">${_("3. File imported")}</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            ${success['message']}
                        </td>
                    </tr>
                </table>
            </td>
            % endif
        </tr>
        <tr>
            <td class="side_spacing">
                <table width="100%">
                    <tr>
                        <td class="imp-header" align="right">
                            <a class="button-a" href="javascript: void(0)" onclick="window.frameElement.close()">${_("Close")}</a>
                            <a class="button-a" href="javascript: void(0)" onclick="do_import();">${_("Import File")}</a>
                        </td>
                        <td width="5%"></td>
                </table>
            </td>
        </tr>
    </table>
</form>
</%def>
