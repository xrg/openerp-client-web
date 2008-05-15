////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://tinyerp.com) All Rights Reserved.
//
// $Id: $
//
// WARNING: This program as such is intended to be used by professional
// programmers who take the whole responsibility of assessing all potential
// consequences resulting from its eventual inadequacies and bugs
// End users who are looking for a ready-to-use solution with commercial
// guarantees and support are strongly advised to contract a Free Software
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
// along with this program; if not, write to the 
// Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
// Boston, MA  02111-1307, USA.
//
////////////////////////////////////////////////////////////////////////////////

function dashboard() {
	
	var tds = [];
	var dbar = getElementsByTagAndClassName('table', 'dashboard')[0];
	
	forEach(getElementsByTagAndClassName('div', 'dashlet', dbar), function(div){
		new Draggable(div, {handle: 'toolbar', starteffect: null, endeffect: null});
		
		if (MochiKit.Base.findIdentical(tds, div.parentNode) == -1) {
			tds.push(div.parentNode);
			div.parentNode.appendChild(SPAN({'class':'dashbar_spacer'}));
			new Droppable(div.parentNode, {ondrop: onDrop});
		}		
	});
	
	function onDrop(src, dst, evt) {

		var xy = MochiKit.DOM.elementPosition(src, dst);
		var ref = null;
						
		var divs = MochiKit.DOM.getElementsByTagAndClassName('div', 'dashlet', dst);
		
		for(var i=0; i < divs.length; i++) {
		
			var el = divs[i];
			var dim = MochiKit.DOM.elementDimensions(el);
			var pos = MochiKit.DOM.elementPosition(el);
								
			if ((pos.y > xy.y) && (xy.y < (pos.y + dim.h))) {
				ref = el;
				break;
			}
		}
						
		dst.insertBefore(src, ref);
		
		src.style.position = 'relative';
		src.style.top = 'auto';
		src.style.left = 'auto';
		src.style.width = '100%';
	}
}

MochiKit.DOM.addLoadEvent(dashboard);
		