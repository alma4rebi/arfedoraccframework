#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  Copyright 2017 youcefsourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
import subprocess
import dnf
import os
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GdkPixbuf, Pango
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location
import time


button_label         = _("Repos Manager")
button_image         = "Antu_distributor-logo-fedora.svg.png"
category             = _("System")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Dnf Repos Manager")
blockclose           = False
if_true_skip         = False
if_false_skip        = os.path.isfile("/usr/bin/dnf")
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
    


class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self._mainbox_.set_border_width(25)
        mainvbox = Gtk.VBox(spacing=5)
        self._mainbox_.pack_start(mainvbox,False,False,0)
        self.base = dnf.Base()
        self.base.read_all_repos()
        self.repos=self.base.repos
        
        headericon   = get_icon_location("fedora.png")
        headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        headerlabel  = Gtk.Label(_("<b>Dnf Repos Manager</b>"),use_markup=True)
        headerlabel.set_line_wrap(True)
        headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        headerlabel.set_max_width_chars(13)
        headerlabel.set_justify(Gtk.Justification.CENTER)
        headerbox.pack_start(headerimage,False,False,0)
        headerbox.pack_start(headerlabel,False,False,0)
        mainvbox.pack_start(headerbox,False,False,0)
        
        mainhbox = Gtk.HBox(spacing=30)
        mainhbox.set_border_width(75)
        mainvbox.pack_start(mainhbox,False,False,0)
        
        mainlabelvbox = Gtk.VBox(spacing=20)
        mainswitchvbox = Gtk.VBox(spacing=16)
        mainhbox.pack_start(mainlabelvbox,True,False,0)
        mainhbox.pack_start(mainswitchvbox,True,False,0)
        
        
        for name,repo in self.repos.items():
            labelhbox = Gtk.HBox()
            label  = Gtk.Label(name)
            label.set_line_wrap(True)
            label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
            headerlabel.set_max_width_chars(40)
            labelhbox.pack_start(label,False,True,0)
            mainlabelvbox.pack_start(labelhbox,False,False,0)
            if not repo.enabled:
                self.switch=Gtk.Switch()
            else:
                self.switch=Gtk.Switch()
                self.switch.set_active(True)
            self.switchhandler=self.switch.connect("state-set",self.on_switch_changed,name)
            switchhbox = Gtk.HBox()
            switchhbox.pack_start(self.switch,True,False,0)
            mainswitchvbox.pack_start(switchhbox,False,False,0)


        

    def on_switch_changed(self,switch,state,reponame):
        if state:
            check = subprocess.call("pkexec dnf config-manager --set-enable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed)
                switch.set_active(False)
                switch.handler_unblock_by_func(self.on_switch_changed)
                return True
                    
        else :
            check = subprocess.call("pkexec dnf config-manager --set-disable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed)
                switch.set_active(True)
                switch.handler_unblock_by_func(self.on_switch_changed)
                return True
 
     
        
        



