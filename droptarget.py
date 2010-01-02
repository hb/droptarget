#!/usr/local/env python
"""inspector for drag'n'drop"""

__version__ = "0.0.1"

import pygtk
pygtk.require('2.0')
import gtk

import sys
from optparse import OptionParser


class MainWindow(object):
    def __init__(self):
        # window
        self._window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self._window.set_size_request(800, 600)
        self._window.connect("destroy", gtk.main_quit)
        self._window.set_border_width(5)
        
        # vbox
        self._vbox = gtk.VBox(False)
        self._window.add(self._vbox)
        
        # drop area
        frame = gtk.Frame()
        self._vbox.pack_start(frame, False)
        eb = gtk.EventBox()
        frame.add(eb)
        label = gtk.Label("drop here")
        eb.add(label)
        # dnd
        eb.drag_dest_set(0, [], 0)
        eb.connect('drag-drop', self._drop_cb)
        eb.connect('drag-motion', self._motion_cb)
        eb.connect('drag-data-received', self._drag_data_received_cb)
        
        # container for targets
        self._target_vbox = gtk.VBox()
        self._vbox.pack_start(self._target_vbox)
        
        self._window.show_all()

    def _drag_data_received_cb(self, widget, context, x, y, selection, targetType, time):
        if selection.target in self._type_dict:
            label = gtk.Label(selection.data.encode('utf8').replace("\r", "").replace("\0", "\\0"))
            label.show()
            self._type_dict[selection.target].add(label)
        
        
    def _motion_cb(self, wid, context, x, y, time):
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True
    
    def _drop_cb(self, wid, context, x, y, time):
        self._type_dict = {}
        for child in self._target_vbox:
            self._target_vbox.remove(child)
        for target in context.targets:
            exp = gtk.Expander(target)
            self._target_vbox.pack_start(exp)
            self._type_dict[target] = exp
            wid.drag_get_data(context, target)
        self._target_vbox.show_all()
        context.finish(True, False, time)
        return True

def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = OptionParser(usage="%prog", version="%prog " + __version__)
    (dummy_opt, dummy_args) = parser.parse_args()
    mainwin = MainWindow()
    gtk.main()
    

if __name__ == "__main__":
    sys.exit(main())