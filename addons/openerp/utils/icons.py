###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
#
# The OpenERP web client is distributed under the "OpenERP Public License".
# It's based on Mozilla Public License Version (MPL) 1.1 with following
# restrictions:
#
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
#     kept as in original distribution without any changes in all software
#     screens, especially in start-up page and the software header, even if
#     the application source code has been changed or updated or code has been
#     added.
#
# -   All distributions of the software must keep source code with OEPL.
#
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################

import os

icons = map(lambda x: (x,x), ['STOCK_ABOUT', 'STOCK_ADD', 'STOCK_APPLY', 'STOCK_BOLD',
'STOCK_CANCEL', 'STOCK_CDROM', 'STOCK_CLEAR', 'STOCK_CLOSE', 'STOCK_COLOR_PICKER',
'STOCK_CONNECT', 'STOCK_CONVERT', 'STOCK_COPY', 'STOCK_CUT', 'STOCK_DELETE',
'STOCK_DIALOG_AUTHENTICATION', 'STOCK_DIALOG_ERROR', 'STOCK_DIALOG_INFO',
'STOCK_DIALOG_QUESTION', 'STOCK_DIALOG_WARNING', 'STOCK_DIRECTORY', 'STOCK_DISCONNECT',
'STOCK_DND', 'STOCK_DND_MULTIPLE', 'STOCK_EDIT', 'STOCK_EXECUTE', 'STOCK_FILE',
'STOCK_FIND', 'STOCK_FIND_AND_REPLACE', 'STOCK_FLOPPY', 'STOCK_GOTO_BOTTOM',
'STOCK_GOTO_FIRST', 'STOCK_GOTO_LAST', 'STOCK_GOTO_TOP', 'STOCK_GO_BACK',
'STOCK_GO_DOWN', 'STOCK_GO_FORWARD', 'STOCK_GO_UP', 'STOCK_HARDDISK',
'STOCK_HELP', 'STOCK_HOME', 'STOCK_INDENT', 'STOCK_INDEX', 'STOCK_ITALIC',
'STOCK_JUMP_TO', 'STOCK_JUSTIFY_CENTER', 'STOCK_JUSTIFY_FILL',
'STOCK_JUSTIFY_LEFT', 'STOCK_JUSTIFY_RIGHT', 'STOCK_MEDIA_FORWARD',
'STOCK_MEDIA_NEXT', 'STOCK_MEDIA_PAUSE', 'STOCK_MEDIA_PLAY',
'STOCK_MEDIA_PREVIOUS', 'STOCK_MEDIA_RECORD', 'STOCK_MEDIA_REWIND',
'STOCK_MEDIA_STOP', 'STOCK_MISSING_IMAGE', 'STOCK_NETWORK', 'STOCK_NEW',
'STOCK_NO', 'STOCK_OK', 'STOCK_OPEN', 'STOCK_PASTE', 'STOCK_PREFERENCES',
'STOCK_PRINT', 'STOCK_PRINT_PREVIEW', 'STOCK_PROPERTIES', 'STOCK_QUIT',
'STOCK_REDO', 'STOCK_REFRESH', 'STOCK_REMOVE', 'STOCK_REVERT_TO_SAVED',
'STOCK_SAVE', 'STOCK_SAVE_AS', 'STOCK_SELECT_COLOR', 'STOCK_SELECT_FONT',
'STOCK_SORT_ASCENDING', 'STOCK_SORT_DESCENDING', 'STOCK_SPELL_CHECK',
'STOCK_STOP', 'STOCK_STRIKETHROUGH', 'STOCK_UNDELETE', 'STOCK_UNDERLINE',
'STOCK_UNDO', 'STOCK_UNINDENT', 'STOCK_YES', 'STOCK_ZOOM_100',
'STOCK_ZOOM_FIT', 'STOCK_ZOOM_IN', 'STOCK_ZOOM_OUT',
'terp-account', 'terp-crm', 'terp-mrp', 'terp-product', 'terp-purchase',
'terp-sale', 'terp-tools', 'terp-administration', 'terp-hr', 'terp-partner',
'terp-project', 'terp-report', 'terp-stock', 'terp-calendar', 'terp-graph',
])

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
        res = "images/stock/%s.png"%(stock_items.get(name, "stock"))

    elif name.startswith('gtk-'):
        res = "images/stock/%s.png"%(name)

    elif name.startswith('terp-'):
        res = "images/icons/%s.png"%(name.replace('terp-', '', 1))

    else:
        name, ext = os.path.splitext(name)
        res = "images/%s%s" % (name, ext or '.png')

    return "/openerp/static/%s" % res


# vim: ts=4 sts=4 sw=4 si et
