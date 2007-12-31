///////////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
//
// $Id$
//
// WARNING: This program as such is intended to be used by professional
// programmers who take the whole responsability of assessing all potential
// consequences resulting from its eventual inadequacies and bugs
// End users who are looking for a ready-to-use solution with commercial
// garantees and support are strongly adviced to contract a Free Software
// Service Company
//
// This program is Free Software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
//
///////////////////////////////////////////////////////////////////////////////

var InfoBox = function(params) {
    this.__init__(params);
}

InfoBox.prototype = {

    __init__ : function(params){
        this.params = MochiKit.Base.update({
            dtStart : null,     // start time
            dtEnd : null,       // end time
            nRecordID : null,   // record id
            title: null,        // title
            description: null   // description
        }, params);

        this.layer = $('calInfoLayer');
        this.box = $('calInfoBox');

        var btnCancel = BUTTON({'class': 'button', 'type': 'button'}, 'Cancel');
        var btnEdit = BUTTON({'class': 'button', 'type': 'button'}, 'Edit');
        var btnDelete = BUTTON({'class': 'button', 'type': 'button'}, 'Delete');

        MochiKit.Signal.connect(btnCancel, 'onclick', this, 'hide');
        MochiKit.Signal.connect(btnEdit, 'onclick', this, 'onEdit');
        MochiKit.Signal.connect(btnDelete, 'onclick', this, 'onDelete');

        var title = this.params.title;                         
        var desc = '(' + this.params.dtStart.strftime('%Y-%m-%d %I:%M %P') + ' - ' + this.params.dtEnd.strftime('%Y-%m-%d %I:%M %P') + ')';

        if (this.params.dtStart.strftime('%Y-%m-%d') == this.params.dtEnd.strftime('%Y-%m-%d')){
            var desc = '(' + this.params.dtStart.strftime('%Y-%m-%d %I:%M %P') + ' - ' + this.params.dtEnd.strftime('%I:%M %P') + ')';
        }

        var desc = SPAN(null, this.params.description, BR(), desc);

        var info = DIV(null,
                    DIV({'class': 'calInfoTitle'}, title),
                    DIV({'class': 'calInfoDesc'}, desc),
                        TABLE({'class': 'calInfoButtons', 'cellpadding': 2}, 
                            TBODY(null, 
                                TR(null,
                                    TD(null, btnEdit), 
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

        setElementDimensions(this.layer, elementDimensions(document.body));
        //setElementDimensions(this.layer, getViewportDimensions());

        var w = 350;
        var h = 125;

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

    onDelete : function(){

        this.hide();

        if (!confirm('Do you realy want to delete this record?')) {
            return false;
        }

        $('_terp_id').value = this.params.nRecordID;
        getCalendar('/calendar/delete/' + $('_terp_calendar_args').value);
    }
}

// vim: sts=4 st=4 et
