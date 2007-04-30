###############################################################################
#
# Copyright (c) 2007 TinyERP Pvt Ltd. (http://tinyerp.com) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################################################

import os

stock_items = {
 'STOCK_YES': 'gtk-yes.png',
 'STOCK_ORIENTATION_PORTRAIT': 'gtk-orientation-portrait.png',
 'STOCK_GO_FORWARD': 'gtk-go-forward-ltr.png',
 'STOCK_CDROM': 'gtk-cdrom.png',
 'STOCK_UNDELETE': 'gtk-undelete-ltr.png',
 'STOCK_EXECUTE': 'gtk-execute.png',
 'STOCK_SAVE': 'gtk-save.png',
 'STOCK_DIALOG_QUESTION': 'gtk-dialog-question.png',
 'STOCK_SORT_ASCENDING': 'gtk-sort-ascending.png',
 'STOCK_REFRESH': 'gtk-refresh.png',
 'STOCK_MEDIA_FORWARD': 'gtk-media-forward-ltr.png',
 'STOCK_STOP': 'gtk-stop.png',
 'STOCK_PRINT_PREVIEW': 'gtk-print-preview.png',
 'STOCK_FIND': 'gtk-find.png',
 'STOCK_PASTE': 'gtk-paste.png',
 'STOCK_ORIENTATION_LANDSCAPE': 'gtk-orientation-landscape.png',
 'STOCK_ZOOM_100': 'gtk-zoom-100.png',
 'STOCK_FIND_AND_REPLACE': 'gtk-find-and-replace.png',
 'STOCK_DIALOG_WARNING': 'gtk-dialog-warning.png',
 'STOCK_ZOOM_IN': 'gtk-zoom-in.png',
 'STOCK_CONVERT': 'gtk-convert.png',
 'STOCK_ITALIC': 'gtk-italic.png',
 'STOCK_MEDIA_RECORD': 'gtk-media-record.png',
 'STOCK_MEDIA_PLAY': 'gtk-media-play-ltr.png',
 'STOCK_OPEN': 'gtk-open.png',
 'STOCK_ORIENTATION_REVERSE_LANDSCAPE': 'gtk-orientation-reverse-landscape.png',
 'STOCK_MEDIA_PREVIOUS': 'gtk-media-previous-ltr.png',
 'STOCK_NEW': 'gtk-new.png',
 'STOCK_CANCEL': 'gtk-cancel.png',
 'STOCK_DISCONNECT': 'gtk-disconnect.png',
 'STOCK_JUSTIFY_LEFT': 'gtk-justify-left.png',
 'STOCK_FILE': 'gtk-file.png',
 'STOCK_QUIT': 'gtk-quit.png',
 'STOCK_EDIT': 'gtk-edit.png',
 'STOCK_CONNECT': 'gtk-connect.png',
 'STOCK_GO_DOWN': 'gtk-go-down.png',
 'STOCK_NETWORK': 'gtk-network.png',
 'STOCK_OK': 'gtk-ok.png',
 'STOCK_GOTO_TOP': 'gtk-goto-top.png',
 'STOCK_ABOUT': 'gtk-about.png',
 'STOCK_COLOR_PICKER': 'gtk-color-picker.png',
 'STOCK_DELETE': 'gtk-delete.png',
 'STOCK_DND': 'gtk-dnd.png',
 'STOCK_CLEAR': 'gtk-clear.png',
 'STOCK_UNINDENT': 'gtk-unindent-ltr.png',
 'STOCK_PREFERENCES': 'gtk-preferences.png',
 'STOCK_HELP': 'gtk-help.png',
 'STOCK_ORIENTATION_REVERSE_PORTRAIT': 'gtk-orientation-reverse-portrait.png',
 'STOCK_SORT_DESCENDING': 'gtk-sort-descending.png',
 'STOCK_ADD': 'gtk-add.png',
 'STOCK_GOTO_LAST': 'gtk-goto-last-ltr.png',
 'STOCK_SELECT_FONT': 'gtk-font.png',
 'STOCK_PROPERTIES': 'gtk-properties.png',
 'STOCK_UNDO': 'gtk-undo-ltr.png',
 'STOCK_SELECT_ALL': 'gtk-select-all.png',
 'STOCK_FLOPPY': 'gtk-floppy.png',
 'STOCK_DIRECTORY': 'gtk-directory.png',
 'STOCK_JUSTIFY_CENTER': 'gtk-justify-center.png',
 'STOCK_GO_BACK': 'gtk-go-back-ltr.png',
 'STOCK_MEDIA_STOP': 'gtk-media-stop.png',
 'STOCK_UNDERLINE': 'gtk-underline.png',
 'STOCK_DND_MULTIPLE': 'gtk-dnd-multiple.png',
 'STOCK_JUSTIFY_FILL': 'gtk-justify-fill.png',
 'STOCK_SPELL_CHECK': 'gtk-spell-check.png',
 'STOCK_LEAVE_FULLSCREEN': 'gtk-leave-fullscreen.png',
 'STOCK_FULLSCREEN': 'gtk-fullscreen.png',
 'STOCK_INDENT': 'gtk-indent-ltr.png',
 'STOCK_APPLY': 'gtk-apply.png',
 'STOCK_ZOOM_OUT': 'gtk-zoom-out.png',
 'STOCK_REVERT_TO_SAVED': 'gtk-revert-to-saved-ltr.png',
 'STOCK_STRIKETHROUGH': 'gtk-strikethrough.png',
 'STOCK_MEDIA_REWIND': 'gtk-media-rewind-ltr.png',
 'STOCK_SELECT_COLOR': 'gtk-select-color.png',
 'STOCK_PRINT': 'gtk-print.png',
 'STOCK_NO': 'gtk-no.png',
 'STOCK_GOTO_FIRST': 'gtk-goto-first-ltr.png',
 'STOCK_MISSING_IMAGE': 'gtk-missing-image.png',
 'STOCK_CLOSE': 'gtk-close.png',
 'STOCK_REMOVE': 'gtk-remove.png',
 'STOCK_CUT': 'gtk-cut.png',
 'STOCK_GO_UP': 'gtk-go-up.png',
 'STOCK_HOME': 'gtk-home.png',
 'STOCK_BOLD': 'gtk-bold.png',
 'STOCK_DIALOG_AUTHENTICATION': 'gtk-dialog-authentication.png',
 'STOCK_ZOOM_FIT': 'gtk-zoom-fit.png',
 'STOCK_INFO': 'gtk-info.png',
 'STOCK_JUMP_TO': 'gtk-jump-to-ltr.png',
 'STOCK_HARDDISK': 'gtk-harddisk.png',
 'STOCK_SAVE_AS': 'gtk-save-as.png',
 'STOCK_DIALOG_INFO': 'gtk-dialog-info.png',
 'STOCK_JUSTIFY_RIGHT': 'gtk-justify-right.png',
 'STOCK_DIALOG_ERROR': 'gtk-dialog-error.png',
 'STOCK_INDEX': 'gtk-index.png',
 'STOCK_GOTO_BOTTOM': 'gtk-goto-bottom.png',
 'STOCK_MEDIA_NEXT': 'gtk-media-next-ltr.png',
 'STOCK_REDO': 'gtk-redo-ltr.png',
 'STOCK_COPY': 'gtk-copy.png',
 'STOCK_MEDIA_PAUSE': 'gtk-media-pause.png'}

gtk_items = {'gtk-media-pause': 'gtk-media-pause.png',
 'gtk-zoom-100': 'gtk-zoom-100.png',
 'gtk-find-and-replace': 'gtk-find-and-replace.png',
 'gtk-leave-fullscreen': 'gtk-leave-fullscreen.png',
 'gtk-yes': 'gtk-yes.png',
 'gtk-add': 'gtk-add.png',
 'gtk-remove': 'gtk-remove.png',
 'gtk-quit': 'gtk-quit.png',
 'gtk-stop': 'gtk-stop.png',
 'gtk-print': 'gtk-print.png',
 'gtk-media-rewind': 'gtk-media-rewind-ltr.png',
 'gtk-goto-top': 'gtk-goto-top.png',
 'gtk-goto-first': 'gtk-goto-first-ltr.png',
 'gtk-go-back': 'gtk-go-back-ltr.png',
 'gtk-orientation-portrait': 'gtk-orientation-portrait.png',
 'gtk-underline': 'gtk-underline.png',
 'gtk-media-next': 'gtk-media-next-ltr.png',
 'gtk-edit': 'gtk-edit.png',
 'gtk-spell-check': 'gtk-spell-check.png',
 'gtk-indent': 'gtk-indent-ltr.png',
 'gtk-directory': 'gtk-directory.png',
 'gtk-revert-to-saved': 'gtk-revert-to-saved-ltr.png',
 'gtk-goto-last': 'gtk-goto-last-ltr.png',
 'gtk-disconnect': 'gtk-disconnect.png',
 'gtk-media-record': 'gtk-media-record.png',
 'gtk-justify-left': 'gtk-justify-left.png',
 'gtk-open': 'gtk-open.png',
 'gtk-sort-ascending': 'gtk-sort-ascending.png',
 'gtk-home': 'gtk-home.png',
 'gtk-ok': 'gtk-ok.png',
 'gtk-dnd': 'gtk-dnd.png',
 'gtk-select-all': 'gtk-select-all.png',
 'gtk-copy': 'gtk-copy.png',
 'gtk-delete': 'gtk-delete.png',
 'gtk-strikethrough': 'gtk-strikethrough.png',
 'gtk-goto-bottom': 'gtk-goto-bottom.png',
 'gtk-media-play': 'gtk-media-play-ltr.png',
 'gtk-color-picker': 'gtk-color-picker.png',
 'gtk-undo': 'gtk-undo-ltr.png',
 'gtk-index': 'gtk-index.png',
 'gtk-cdrom': 'gtk-cdrom.png',
 'gtk-dialog-question': 'gtk-dialog-question.png',
 'gtk-zoom-out': 'gtk-zoom-out.png',
 'gtk-apply': 'gtk-apply.png',
 'gtk-save-as': 'gtk-save-as.png',
 'gtk-floppy': 'gtk-floppy.png',
 'gtk-find': 'gtk-find.png',
 'gtk-paste': 'gtk-paste.png',
 'gtk-info': 'gtk-info.png',
 'gtk-save': 'gtk-save.png',
 'gtk-cut': 'gtk-cut.png',
 'gtk-justify-right': 'gtk-justify-right.png',
 'gtk-about': 'gtk-about.png',
 'gtk-close': 'gtk-close.png',
 'gtk-bold': 'gtk-bold.png',
 'gtk-convert': 'gtk-convert.png',
 'gtk-network': 'gtk-network.png',
 'gtk-zoom-in': 'gtk-zoom-in.png',
 'gtk-media-previous': 'gtk-media-previous-ltr.png',
 'gtk-go-forward': 'gtk-go-forward-ltr.png',
 'gtk-italic': 'gtk-italic.png',
 'gtk-refresh': 'gtk-refresh.png',
 'gtk-unindent': 'gtk-unindent-ltr.png',
 'gtk-undelete': 'gtk-undelete-ltr.png',
 'gtk-jump-to': 'gtk-jump-to-ltr.png',
 'gtk-go-up': 'gtk-go-up.png',
 'gtk-harddisk': 'gtk-harddisk.png',
 'gtk-no': 'gtk-no.png',
 'gtk-dnd-multiple': 'gtk-dnd-multiple.png',
 'gtk-select-color': 'gtk-select-color.png',
 'gtk-zoom-fit': 'gtk-zoom-fit.png',
 'gtk-media-forward': 'gtk-media-forward-ltr.png',
 'gtk-file': 'gtk-file.png',
 'gtk-properties': 'gtk-properties.png',
 'gtk-fullscreen': 'gtk-fullscreen.png',
 'gtk-redo': 'gtk-redo-ltr.png',
 'gtk-missing-image': 'gtk-missing-image.png',
 'gtk-orientation-reverse-portrait': 'gtk-orientation-reverse-portrait.png',
 'gtk-orientation-reverse-landscape': 'gtk-orientation-reverse-landscape.png',
 'gtk-preferences': 'gtk-preferences.png',
 'gtk-orientation-landscape': 'gtk-orientation-landscape.png',
 'gtk-select-font': 'gtk-font.png',
 'gtk-sort-descending': 'gtk-sort-descending.png',
 'gtk-print-preview': 'gtk-print-preview.png',
 'gtk-cancel': 'gtk-cancel.png',
 'gtk-connect': 'gtk-connect.png',
 'gtk-dialog-error': 'gtk-dialog-error.png',
 'gtk-execute': 'gtk-execute.png',
 'gtk-go-down': 'gtk-go-down.png',
 'gtk-dialog-warning': 'gtk-dialog-warning.png',
 'gtk-dialog-info': 'gtk-dialog-info.png',
 'gtk-media-stop': 'gtk-media-stop.png',
 'gtk-help': 'gtk-help.png',
 'gtk-justify-center': 'gtk-justify-center.png',
 'GTK_STOCK_DIALOG_AUTHENTICATION': 'gtk-dialog-authentication.png',
 'gtk-clear': 'gtk-clear.png',
 'gtk-justify-fill': 'gtk-justify-fill.png',
 'gtk-new': 'gtk-new.png'}

def get_icon(name):

    if name.startswith('STOCK_'):
        return "/static/images/stock/%s"%(stock_items.get(name, "stock.png"))

    if name.startswith('gtk-'):
        return "/static/images/stock/%s"%(gtk_items.get(name, "stock.png"))

    if name.startswith('terp-'):
        return "/static/images/icons/%s.png"%(name.replace('terp-', '', 1))

    name, ext = os.path.splitext(name)
    return "/static/images/%s.%s" % (name, ext or 'png')
