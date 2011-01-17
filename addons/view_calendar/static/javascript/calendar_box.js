////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY OpenERP SA. All Rights Reserved.
//
// $Id$
//
// Developed by OpenERP (http://openerp.com) and Axelor (http://axelor.com).
//
// The OpenERP web client is distributed under the "OpenERP Public License".
// It's based on Mozilla Public License Version (MPL) 1.1 with following 
// restrictions:
//
// -   All names, links and logos of OpenERP must be kept as in original
//     distribution without any changes in all software screens, especially
//     in start-up page and the software header, even if the application
//     source code has been changed or updated or code has been added.
//
// You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
//
////////////////////////////////////////////////////////////////////////////////

var InfoBox = function(params) {
    this.__init__(params);
};

InfoBox.prototype = {

    __init__ : function(params){
        this.params = MochiKit.Base.update({
            dtStart : null,     // start time
            dtEnd : null,       // end time
            nRecordID : null,   // record id
            title: null,        // title
            description: null,   // description
            event_id: null,      // id
            create_date: null,   //create date
            create_uid: null,    //create uid
            write_date: null,    //write date
            write_uid: null      //write uid
        }, params);

        this.layer = openobject.dom.get('calInfoLayer');
        this.box = openobject.dom.get('calInfoBox');

//        var btnCancel = BUTTON({'class': 'button', 'type': 'button'}, _('Cancel'));
//        var btnEdit = BUTTON({'class': 'button', 'type': 'button'}, _('Edit'));
//        var btnCopy = BUTTON({'class': 'button', 'type': 'button'}, _('Duplicate'));
//        var btnDelete = BUTTON({'class': 'button', 'type': 'button'}, _('Delete'));
        
        var btnCancel = A({'class': 'button-a', 'href': 'javascript: void(0)'}, _('Cancel'));
        var btnEdit = A({'class': 'button-a', 'href': 'javascript: void(0)'}, _('Edit'));
        var btnCopy = A({'class': 'button-a', 'href': 'javascript: void(0)'}, _('Duplicate'));
        var btnDelete = A({'class': 'button-a', 'href': 'javascript: void(0)'}, _('Delete'));
        
        MochiKit.Signal.connect(btnCancel, 'onclick', this, 'hide');
        MochiKit.Signal.connect(btnEdit, 'onclick', this, 'onEdit');
        MochiKit.Signal.connect(btnCopy, 'onclick', this, 'onCopy');
        MochiKit.Signal.connect(btnDelete, 'onclick', this, 'onDelete');
        
        var DT_FORMAT = '%Y-%m-%d';
        var H_FORMAT = '%I:%M %P';

        DTH_FORMAT = openobject.dom.get('calGantt') ? getNodeAttribute('calGantt', 'dtFormat') :
                        openobject.dom.get('calMonth') ? getNodeAttribute('calMonth', 'dtFormat') : 
                            openobject.dom.get('calWeek') ? getNodeAttribute('calWeek', 'dtFormat') : DT_FORMAT;

        var DTH_FORMAT = DT_FORMAT + ' ' + H_FORMAT;

        var title = this.params.title;                         
        var desc = '(' + this.params.dtStart.strftime(DTH_FORMAT) + ' - ' + this.params.dtEnd.strftime(DTH_FORMAT) + ')';

        if (this.params.dtStart.strftime(DT_FORMAT) == this.params.dtEnd.strftime(DT_FORMAT)){
            var desc = '(' + this.params.dtStart.strftime(DTH_FORMAT) + ' - ' + this.params.dtEnd.strftime(H_FORMAT) + ')';
        }

        var desc = SPAN(null, this.params.description, BR(), desc);
        
        var log = DIV({'class': 'calLogInfo'},
                        DIV(null, 'ID:', this.params.event_id),
                        DIV(null, _('Creation User: '), this.params.create_uid),
                        DIV(null, _('Creation Date: '), this.params.create_date),
                        DIV(null, _('Latest Modification by: '), this.params.write_uid),
                        DIV(null, _('Latest Modification Date: '), this.params.write_date)
                     );
        var info = DIV(null,
                    DIV({'class': 'calInfoTitle'}, title),
                    DIV({'class': 'calInfoDesc'}, desc),
                    DIV(null, log),
                        TABLE({'class': 'calInfoButtons', 'cellpadding': 2}, 
                            TBODY(null, 
                                TR(null,
                                    TD(null, btnEdit),
                                    TD(null, btnCopy),
                                    TD(null, btnDelete),
                                    TD({'align': 'right', 'width': '100%'}, btnCancel)))));

        if (!this.layer) {
            this.layer = DIV({id: 'calInfoLayer'});
            appendChildNodes(document.body, this.layer);
            setOpacity(this.layer, 0.3);
            connect(this.layer, 'onclick', this, 'hide');
        }

        if (!this.box) {
            this.box = DIV({id: 'calInfoBox'});
            appendChildNodes(document.body, this.box);
        }

        this.box.innerHTML = "";

        appendChildNodes(this.box, info);
    },

    show : function(evt) {

    	jQuery(this.layer).height(jQuery(document).height());
    	
        var w = 350;
        var h = 145;

        setElementDimensions(this.box, {w: w, h: h});

        var x = evt.mouse().page.x;
        var y = evt.mouse().page.y;

        x -= w / 2;
        y -= h - h / 3;

        var vd = elementDimensions(document.body);
        var md = elementDimensions(this.box);

        if ((x + md.w) > vd.w) {
            x -= x + md.w - vd.w;
        }

        x = Math.max(0, x);
        y = Math.max(0, y);

        setElementPosition(this.box, {x: x, y: y});

        showElement(this.layer);
        showElement(this.box);
    },

    hide : function(evt) {
        hideElement(this.box);
        hideElement(this.layer);
    },

    onEdit : function(){
        this.hide();
        editCalendarRecord(this.params.nRecordID);
    },
    
    onCopy : function(){
        this.hide();
        var req = copyCalendarRecord(this.params.nRecordID);
        req.addCallback(function(res){
            getCalendar();
        });
    },

    onDelete : function(){

        this.hide();

        if (!confirm(_('Do you really want to delete this record?'))) {
            return false;
        }

        var params = getFormParams('_terp_concurrency_info');
        MochiKit.Base.update(params, {
           '_terp_id': this.params.nRecordID,
           '_terp_model': openobject.dom.get('_terp_model').value,
           '_terp_context': openobject.dom.get('_terp_context').value
        });

        var req = openobject.http.postJSON('/view_calendar/calendar/delete', params);
        var self = this;

        req.addCallback(function(obj){

           if (obj.error) {
               return error_display(obj.error);
           }

           var id = parseInt(openobject.dom.get('_terp_id').value) || 0;
           var ids = [];

           try {
               ids = eval('(' + openobject.dom.get('_terp_ids').value + ')') || [];
           }catch(e){}

           var idx = MochiKit.Base.findIdentical(ids, self.params.nRecordID);

           if (id == self.params.nRecordID) {
               openobject.dom.get('_terp_id').value = 'False';
           }

           if (idx > -1) {
               ids = ids.splice(idx, 1);
               openobject.dom.get('_terp_ids').value = '[' + ids.join(', ') + ']';
           }

           getCalendar();
        });
    }
};
