###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt. Ltd. (http://openerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.
#
###############################################################################

import os

stock_items = {
'STOCK_ABOUT' : 'gtk-about',
'STOCK_ADD' : 'gtk-add',
'STOCK_APPLY' : 'gtk-apply',
'STOCK_BOLD' : 'gtk-bold',
'STOCK_CANCEL' : 'gtk-cancel',
'STOCK_CDROM' : 'gtk-cdrom',
'STOCK_CLEAR' : 'gtk-clear',
'STOCK_CLOSE' : 'gtk-close',
'STOCK_COLOR_PICKER' : 'gtk-color-picker',
'STOCK_CONVERT' : 'gtk-convert',
'STOCK_CONNECT' : 'gtk-connect',
'STOCK_COPY' : 'gtk-copy',
'STOCK_CUT' : 'gtk-cut',
'STOCK_DELETE' : 'gtk-delete',
'STOCK_DIALOG_AUTHENTICATION' : 'gtk-dialog-authentication',
'STOCK_DIALOG_ERROR' : 'gtk-dialog-error',
'STOCK_DIALOG_INFO' : 'gtk-dialog-info',
'STOCK_DIALOG_QUESTION' : 'gtk-dialog-question',
'STOCK_DIALOG_WARNING' : 'gtk-dialog-warning',
'STOCK_DIRECTORY' : 'gtk-directory',
'STOCK_DISCONNECT' : 'gtk-disconnect',
'STOCK_DND' : 'gtk-dnd',
'STOCK_DND_MULTIPLE' : 'gtk-dnd-multiple',
'STOCK_EDIT' : 'gtk-edit',
'STOCK_EXECUTE' : 'gtk-execute',
'STOCK_FILE' : 'gtk-file',
'STOCK_FIND' : 'gtk-find',
'STOCK_FIND_AND_REPLACE' : 'gtk-find-and-replace',
'STOCK_FLOPPY' : 'gtk-floppy',
'STOCK_FULLSCREEN' : 'gtk-fullscreen',
'STOCK_GOTO_BOTTOM' : 'gtk-goto-bottom',
'STOCK_GOTO_FIRST' : 'gtk-goto-first',
'STOCK_GOTO_LAST' : 'gtk-goto-last',
'STOCK_GOTO_TOP' : 'gtk-goto-top',
'STOCK_GO_BACK' : 'gtk-go-back',
'STOCK_GO_DOWN' : 'gtk-go-down',
'STOCK_GO_FORWARD' : 'gtk-go-forward',
'STOCK_GO_UP' : 'gtk-go-up',
'STOCK_HARDDISK' : 'gtk-harddisk',
'STOCK_HELP' : 'gtk-help',
'STOCK_HOME' : 'gtk-home',
'STOCK_INDENT' : 'gtk-indent',
'STOCK_INDEX' : 'gtk-index',
'STOCK_INFO' : 'gtk-info',
'STOCK_ITALIC' : 'gtk-italic',
'STOCK_JUMP_TO' : 'gtk-jump-to',
'STOCK_JUSTIFY_CENTER' : 'gtk-justify-center',
'STOCK_JUSTIFY_FILL' : 'gtk-justify-fill',
'STOCK_JUSTIFY_LEFT' : 'gtk-justify-left',
'STOCK_JUSTIFY_RIGHT' : 'gtk-justify-right',
'STOCK_LEAVE_FULLSCREEN' : 'gtk-leave-fullscreen',
'STOCK_MEDIA_FORWARD' : 'gtk-media-forward',
'STOCK_MEDIA_NEXT' : 'gtk-media-next',
'STOCK_MEDIA_PAUSE' : 'gtk-media-pause',
'STOCK_MEDIA_PLAY' : 'gtk-media-play',
'STOCK_MEDIA_PREVIOUS' : 'gtk-media-previous',
'STOCK_MEDIA_RECORD' : 'gtk-media-record',
'STOCK_MEDIA_REWIND' : 'gtk-media-rewind',
'STOCK_MEDIA_STOP' : 'gtk-media-stop',
'STOCK_MISSING_IMAGE' : 'gtk-missing-image',
'STOCK_NETWORK' : 'gtk-network',
'STOCK_NEW' : 'gtk-new',
'STOCK_NO' : 'gtk-no',
'STOCK_OK' : 'gtk-ok',
'STOCK_OPEN' : 'gtk-open',
'STOCK_PASTE' : 'gtk-paste',
'STOCK_PREFERENCES' : 'gtk-preferences',
'STOCK_PRINT' : 'gtk-print',
'STOCK_PRINT_PREVIEW' : 'gtk-print-preview',
'STOCK_PROPERTIES' : 'gtk-properties',
'STOCK_QUIT' : 'gtk-quit',
'STOCK_REDO' : 'gtk-redo',
'STOCK_REFRESH' : 'gtk-refresh',
'STOCK_REMOVE' : 'gtk-remove',
'STOCK_REVERT_TO_SAVED' : 'gtk-revert-to-saved',
'STOCK_SAVE' : 'gtk-save',
'STOCK_SAVE_AS' : 'gtk-save-as',
'STOCK_SELECT_COLOR' : 'gtk-select-color',
'STOCK_SELECT_FONT' : 'gtk-select-font',
'STOCK_SORT_ASCENDING' : 'gtk-sort-ascending',
'STOCK_SORT_DESCENDING' : 'gtk-sort-descending',
'STOCK_SPELL_CHECK' : 'gtk-spell-check',
'STOCK_STOP' : 'gtk-stop',
'STOCK_STRIKETHROUGH' : 'gtk-strikethrough',
'STOCK_UNDELETE' : 'gtk-undelete',
'STOCK_UNDERLINE' : 'gtk-underline',
'STOCK_UNDO' : 'gtk-undo',
'STOCK_UNINDENT' : 'gtk-unindent',
'STOCK_YES' : 'gtk-yes',
'STOCK_ZOOM_100' : 'gtk-zoom-100',
'STOCK_ZOOM_FIT' : 'gtk-zoom-fit',
'STOCK_ZOOM_IN' : 'gtk-zoom-in',
'STOCK_ZOOM_OUT' : 'gtk-zoom-out',
}

def get_icon(name):

    if name.startswith('STOCK_'):
        return "/static/images/stock/%s.png"%(stock_items.get(name, "stock"))

    if name.startswith('gtk-'):
        return "/static/images/stock/%s.png"%(name)

    if name.startswith('terp-'):
        return "/static/images/icons/%s.png"%(name.replace('terp-', '', 1))

    name, ext = os.path.splitext(name)
    return "/static/images/%s%s" % (name, ext or '.png')
