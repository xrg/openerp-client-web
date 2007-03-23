///////////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
//
// $Id: list.py 5 2007-03-23 06:13:51Z ame $
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

/**
 * Configuration settings for TinyAjax
 *
 */
var TinyAjaxConfig = {
	status: "Loading...",			// The message to display
	statusElem: "load_status",		// The element id in which message should be display
	target: null					// Target element id where result should go
}

/**
 * A wrapper arround MochiKit's doSimpleXMLHttpRequest method.
 * Provides a way to display Google style fancy "Loading..." message.
 *
 */
var TinyAjax = {

	/**
	 * A wrapper arround doSimpleXMLHttpRequest
	 *
	 * @param url the url
	 * @param params request paramas as map
	 * @param update the element id where result should go
	 * @param message the loading message
	 * @return differed object with wait(sec) function
	 *
	 */
	request: function(url, params, update, message) {

		$(TinyAjaxConfig.statusElem).innerHTML = message ? message : TinyAjaxConfig.status;
		$(TinyAjaxConfig.statusElem).style.display = "block";

		res = doSimpleXMLHttpRequest(url, params);

		res.addCallback(function(xmlHttp){
			target = update ? update : TinyAjaxConfig.target;
			if (target) {
				$(target).innerHTML = xmlHttp.responseText;
			}
		});

		res.addBoth(function(xmlHttp){
			$(TinyAjaxConfig.statusElem).style.display = "none";
		});

		res.wait = function(sec){
			return wait(sec, res);
		}

		return res;
	}
}

/**
 * A function to open centered popup window
 *
 */
function wopen(url, name, w, h) {
    var width = w ? w : 400;
    var height = h ? h : 300;
    var left = parseInt((screen.availWidth/2) - (width/2));
    var top = parseInt((screen.availHeight/2) - (height/2));
    var windowFeatures = "toolbar=0, statusbar=0, scrollbars=1" + ",width=" + width + ",height=" + height +
        ",status,resizable,left=" + left + ",top=" + top +
        "screenX=" + left + ",screenY=" + top;
    return window.open(url, name ? name : "popup", windowFeatures);
}

function URL(path, args) {
	return args ? path + "?" + queryString(args) : path;
}

