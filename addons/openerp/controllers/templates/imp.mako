<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>Import Data</title>

	<link rel="stylesheet" type="text/css" href="/openerp/static/css/impex.css"/>

    <script type="text/javascript">
        function add_fields(){
        
            var tree = treeGrids['${tree.name}'];
            
            var fields = tree.selection;
            var select = openobject.dom.get('fields');

            var opts = {};
            forEach(openobject.dom.get('fields').options, function(o){
                opts[o.value] = o;
            });

            forEach(fields, function(f){

                var text = f.record.items.name;
                var id = f.record.id;

                if (id in opts) return;

                select.options.add(new Option(text, id));
            });
        }

        function del_fields(all){

            var fields = filter(function(o){return o.selected;}, openobject.dom.get('fields').options);

            if (all){
                openobject.dom.get('fields').innerHTML = '';
            } else {
                forEach(fields, function(f){
                    removeElement(f);
                });
            }
        }

        function do_import(form){

            var options = openobject.dom.get('fields').options;

            forEach(options, function(o){
                o.selected = true;
            });

            jQuery('#'+form).attr({
                'target': "detector",
                'action': openobject.http.getURL('/openerp/impex/import_data')
            }).submit();
        }

        function on_detector(src){
            var d = openobject.dom.get("detector");

            if (d.contentDocument)
                d = d.contentDocument;
            else if (d.contentWindow)
                d = d.contentWindow.document;
            else
                d = d.document;

            var f = d.getElementById('fields');

            if (f) {
                openobject.dom.get('fields').innerHTML = '';
                forEach(f.options, function(o){
                    openobject.dom.get('fields').options.add(new Option(o.text, o.value));
                });
            } else {
                f = d.getElementsByTagName('pre');
                if (f[0]) error_display(f[0].innerHTML);
            }
        }

        function do_autodetect(form){

            if (! openobject.dom.get('csvfile').value ){
                return error_display(_('You must select an import file first.'));
            }

            jQuery('#'+form).attr({
                'target': "detector",
                'action': openobject.http.getURL('/openerp/impex/detect_data')
            }).submit();
        }

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
                    	<td class="imp-header" align="left">
                            <a class="button-a" href="javascript: void(0)" onclick="do_import('import_data');">${_("Import")}</a>
                            <a class="button-a" href="javascript: void(0)" onclick="window.close()">${_("Close")}</a>
                        </td>
                        <td align="center" class="pop_head_font">${_("Import Data")}</td>
                        <td width="30%"></td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
                <table class="fields-selector-import" cellspacing="5" border="0">
                    <tr>
                        <th class="fields-selector-left">${_("All fields")}</th>
                        <th class="fields-selector-center">&nbsp;</th>
                        <th class="fields-selector-right">${_("Fields to import")}</th>
                    </tr>
                    <tr>
                        <td class="fields-selector-left" height="300px">
                            <div id="fields_left">${tree.display()}</div>
                        </td>
                        <td class="fields-selector-center">
                        	<table border="0" cellpadding="0" cellspacing="0" width="100%">
                        		<tr>
                        			<td align="center">
                        				<a class="button-a" href="javascript: void(0)" onclick="add_fields()">${_("Add")}</a>
                        			</td>
                        		</tr>
                        		<tr>
                        			<td align="center">
                        				<a class="button-a" href="javascript: void(0)" onclick="del_fields()">${_("Remove")}</a>
                        			</td>
                        		</tr>
                        		<tr>
                        			<td align="center">
                        				<a class="button-a" href="javascript: void(0)" onclick="del_fields(true)">${_("Nothing")}</a>
                        			</td>
                        		</tr>
                        		<tr>
                        			<td align="center">
                        				<a class="button-a" href="javascript: void(0)" onclick="do_autodetect('import_data')">${_("Auto Detect")}</a>
                        			</td>
                        		</tr>
                        	</table>
                        </td>
                        <td class="fields-selector-right" height="300px">
                            <select name="fields" id="fields" multiple="multiple">
                                % for f in fields or []:
                                <option value="${f[0]}">${f[1]}</option>
                                % endfor
                            </select>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
                <fieldset>
                    <legend>${_("File to import")}</legend>
                    <input type="file" id="csvfile" size="50" name="csvfile" onchange="do_autodetect('import_data')"/>
                </fieldset>
            </td>
        </tr>
        <tr>
            <td class="side_spacing">
                <fieldset>
                    <legend>${_("Options")}</legend>
                    <table>
                        <tr>
                            <td class="label">${_("Separator:")}</td>
                            <td><input type="text" name="csvsep" value=","/></td>
                            <td class="label">${_("Delimiter:")}</td>
                            <td><input type="text" name="csvdel" value='"'/></td>
                        </tr>
                        <tr>
                            <td class="label">${_("Encoding:")}</td>
                            <td>
                                <select name="csvcode">
                                    <option value="utf-8">UTF-8</option>
                                    <option value="latin1">Latin 1</option>
                                </select>
                            </td>
                            <td class="label">${_("Lines to skip:")}</td>
                            <td><input type="text" name="csvskip" value="1"/></td>
                        </tr>
                    </table>
                </fieldset>
            </td>
        </tr>
    </table>
</form>

<iframe name="detector" id="detector" style="display: none;" src="about:blank" onload="on_detector(this)"/>
</%def>
