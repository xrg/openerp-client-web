<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>Import Data</title>
    <link href="/static/css/listgrid.css" rel="stylesheet" type="text/css"/>
    <script type="text/javascript" src="/static/javascript/listgrid.js"></script>

    <style type="text/css">
        .fields-selector {
            width: 100%;
            height: 300px;
        }

        .fields-selector-left {
            width: 45%;
        }

        .fields-selector-center {
            width: 10%;
        }

        .fields-selector-right {
            width: 45%;
        }

        .fields-selector select {
            width: 100%;
            height: 100%;
        }

        .fields-selector button {
            width: 100%;
            margin: 5px 0px;
        }
    </style>

    <script type="text/javascript">
        function add_fields(){
        
            var tree = ${tree.field_id};
            
            var fields = tree.selection;
            var select = $('fields');

            var opts = {};
            forEach($('fields').options, function(o){
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

            var fields = filter(function(o){return o.selected;}, $('fields').options);

            if (all){
                $('fields').innerHTML = '';
            } else {
                forEach(fields, function(f){
                    removeElement(f);
                });
            }
        }

        function do_import(form){

            var options = $('fields').options;

            forEach(options, function(o){
                o.selected = true;
            });

            form.target = "detector";

            setNodeAttribute(form, 'action', '/impex/import_data');
            form.submit();
        }

        function on_detector(src){
            var d = $("detector");

            if (d.contentDocument)
                d = d.contentDocument;
            else if (d.contentWindow)
                d = d.contentWindow.document;
            else
                d = d.document;

            var f = d.getElementById('fields');

            if (f) {
                $('fields').innerHTML = '';
                forEach(f.options, function(o){
                    $('fields').options.add(new Option(o.text, o.value));
                });
            } else {
                f = d.getElementsByTagName('pre');
                if (f[0]) alert(f[0].innerHTML);
            }
        }

        function do_autodetect(form){

            if (! $('csvfile').value ){
                return alert('You must select an import file first!');
            }

            form.target = "detector";

            setNodeAttribute(form, 'action','/impex/detect_data');
            form.submit();
        }

    </script>
</head>
<body>

<form action="/impex/import_data" method="post" enctype="multipart/form-data">

    <input type="hidden" id="_terp_source" name="_terp_source" value="${source}"/>
    <input type="hidden" id="_terp_model" name="_terp_model" value="${model}"/>
    <input type="hidden" id="_terp_ids" name="_terp_ids" value="[]"/>
    <input type="hidden" id="_terp_fields2" name="_terp_fields2" value="[]"/>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/stock/gtk-go-down.png"/>
                        </td>
                        <td width="100%">Import Data</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <table class="fields-selector" cellspacing="5" border="0">
                    <tr>
                        <th class="fields-selector-left">All fields</th>
                        <th class="fields-selector-center">&nbsp;</th>
                        <th class="fields-selector-right">Fields to import</th>
                    </tr>
                    <tr>
                        <td class="fields-selector-left" height="300px">
                            <div py:content="tree.display()" style="overflow: scroll; width: 100%; height: 100%; border: solid #999999 1px;"/>
                        </td>
                        <td class="fields-selector-center">
                            <button type="button" onclick="add_fields()">Add</button><br/>
                            <button type="button" onclick="del_fields()">Remove</button><br/>
                            <button type="button" onclick="del_fields(true)">Nothing</button>
                            <br/><br/>
                            <button type="button" onclick="do_autodetect(form)">Auto Detect</button>
                        </td>
                        <td class="fields-selector-right" height="300px">
                            <select name="fields" id="fields" multiple="multiple">
                                <option py:for="f in value_of('fields', [])" py:content="f[1]" value="${f[0]}"></option>
                            </select>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <fieldset>
                    <legend>File to import</legend>
                    <input type="file" id="csvfile" name="csvfile" onchange="do_autodetect(form)"/>
                </fieldset>
            </td>
        </tr>
        <tr>
            <td>
                <fieldset>
                    <legend>Options</legend>
                    <table>
                        <tr>
                            <td class="label">Separator: </td>
                            <td><input type="text" name="csvsep" value=","/></td>
                            <td class="label">Delimiter: </td>
                            <td><input type="text" name="csvdel" value='"'/></td>
                        </tr>
                        <tr>
                            <td class="label">Encoding: </td>
                            <td>
                                <select name="csvcode">
                                    <option value="utf-8">UTF-8</option>
                                    <option value="latin1">Latin 1</option>
                                </select>
                            </td>
                            <td class="label">Lines to skip: </td>
                            <td><input type="text" name="csvskip" value="1"/></td>
                        </tr>
                    </table>
                </fieldset>
            </td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="100%">&nbsp;</td>
                            <td><button type="button" onclick="do_import(form)">Import</button></td>
                            <td><button type="button" onclick="window.close()">Close</button></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</form>

<iframe name="detector" id="detector" style="display: none;" src="about:blank" onload="on_detector(this)"/>

</body>
</html>
