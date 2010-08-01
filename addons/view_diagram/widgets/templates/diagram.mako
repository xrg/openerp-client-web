<script type="text/javascript">

    var WORKFLOW;
    
    jQuery(document).ready(function(){
        WORKFLOW = new openobject.workflow.Workflow('canvas');
        WORKFLOW.setViewPort("viewport");
    });
    
</script>

<table width="100%">
    <tr>
        <td style="padding: 0px;">
            <table width="100%">
                <tr>
                    <input type="hidden" id="wkf_id" name="wkf_id" value="${dia_id}"/>
                    <input type="hidden" id="node" name="node" value="${node}"/>
                    <input type="hidden" id="connector" name="connector" value="${connector}"/>
                    <input type="hidden" id="src_node" name="src_node" value="${src_node}"/>
                    <input type="hidden" id="des_node" name="des_node" value="${des_node}"/>
                    <input type="hidden" id="node_flds_visible" name="node_flds_visible" value="${node_flds['visible']}"/>
                    <input type="hidden" id="node_flds_invisible" name="node_flds_invisible" value="${node_flds['invisible']}"/>
                    <input type="hidden" id="bgcolors" name="bgcolors" value="${bgcolor}"/>
                    <input type="hidden" id="shapes" name="shapes" value="${shapes}"/>
                    <input type="hidden" id="conn_flds" name="conn_flds" value="${conn_flds}"/>
                    
                    <td width="36px" valign="top" id="toolbox"></td>
                    <td height="100%" width="100%" valign="top" style="padding: 0px;">                        
                        <div id="viewport" style="position: relative; width: 100%; height: 550px; border: 1px solid gray; overflow: auto;">
                            <div id="canvas" style="position: absolute;  width: auto; height: auto;">
                                <span id="loading" style="color: red; width:100%;" align="right">${_("Loading...")}</span>
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr class="toolbar">
        <td align="left" id="status" style="width: 100%; height: 24px; background-color: #808080;">&nbsp;</td>                       
    </tr>
</table>
