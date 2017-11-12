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
import os
import sys
from  arfedoraccframework import plugins_loader
from  arfedoraccframework.baseutils import arch, get_distro_name, get_distro_version
from arfedoraccframework.appinformation  import authors_, version_, copyright_, comments_, website_,icon_, translators_, \
appname, appwindowtitle, appid, homedata, mainbuttonsizewidth, mainbuttonsizeheight, mainbuttonbold, maxwidgetinrow
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gio,GdkPixbuf,GLib,Pango





MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""

        
        

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_category = {}
        #self.set_border_width(10)
        self.set_size_request(800, 610)
        #self.set_resizable(False)
        
        
        
        self.header=Gtk.HeaderBar()
        self.header.set_title(appwindowtitle.title())
        self.header.set_show_close_button(True)
        self.headerhbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.header.pack_start(self.headerhbox)
        self.set_titlebar(self.header)
        
        sw=Gtk.ScrolledWindow()
        self.maincontainer = Gtk.VBox(spacing=10)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.row = Gtk.ListBoxRow(activatable=False)
        self.row.add(self.maincontainer)
        listbox.add(self.row)
        sw.add(listbox)
        self.add(sw)


        all_plugins=plugins_loader.get_plugins()
        for module_name in all_plugins:
            plugin = plugins_loader.load_plugin(module_name)
            if not plugin:
                continue
            try:
                priority             = plugin.priority
                if_true_skip         = plugin.if_true_skip
                if_false_skip        = plugin.if_false_skip
                if_one_true_skip     = plugin.if_one_true_skip
                if_all_true_skip     = plugin.if_all_true_skip
                if if_true_skip:
                    continue
                if not if_false_skip:
                    continue
                if any(if_one_true_skip):
                    continue
                if all(if_all_true_skip):
                    continue



                arch_                = plugin.arch
                distro_name_         = plugin.distro_name
                distro_version_      = plugin.distro_version
                if "all" not in arch_:
                    if arch not in arch_:
                        continue
                if "all" not in distro_name_:
                    if get_distro_name() not in distro_name_:
                        continue                 
                if "all" not in distro_version_:
                    if get_distro_version() not in distro_version_:
                        continue
                title                = plugin.title
                blockclose           = plugin.blockclose
                mainbuttontooltip    = plugin.mainbuttontooltip
                button_label         = plugin.button_label
                button_image         =  [l for l in [os.path.join(homedata+"/icons",plugin.button_image),os.path.join("/usr/share/{}/icons".format(appname),plugin.button_image)] if os.path.isfile(l)]
                if len(button_image)!=0:
                    pixbuf=GdkPixbuf.Pixbuf.new_from_file_at_size(button_image[0],mainbuttonsizewidth,mainbuttonsizeheight)
                    image          = Gtk.Image.new_from_pixbuf(pixbuf)
                category             = plugin.category
                if category not in all_category.keys():
                    category_label = Gtk.Label("<b>"+category+"</b>",use_markup=True)
                    hseparator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
                    hseparator.set_margin_top(30)
                    vmaincategorybox = Gtk.VBox(spacing=3)
                    hh2categorybox = Gtk.HBox(spacing=13)
                    
                    h1categorybox = Gtk.HBox()
                    v1categorybox = Gtk.VBox()
                    all_category.setdefault(category,[hh2categorybox,vmaincategorybox])
                    
                    h1categorybox.pack_start(category_label,False,False,0)
                    v1categorybox.pack_start(hseparator,False,False,0)
                    vmaincategorybox.pack_start(h1categorybox,False,False,0)
                    vmaincategorybox.pack_start(hh2categorybox,False,False,0)
                    self.maincontainer.pack_start(vmaincategorybox,False,False,0)
                    self.maincontainer.pack_start(v1categorybox,False,False,0)
                    

                vh2categorybox = Gtk.VBox(spacing=13)
                h2categorybox = Gtk.HBox(spacing=10)
                vh2categorybox.pack_start(h2categorybox,False,False,0)
                all_category[category][0].pack_start(vh2categorybox,False,False,0)
                         
            except Exception as e:
                print(e)
                print("Ignored >> Load {} Fail.".format(plugin))
                continue

            if priority==1:
                try:
                    plg= plugin.Plugin(self,self.row)
                except:
                    print("Ignored >> Load {} Fail.".format(module_name))
                    continue
            elif priority>1:
                try:
                    run_function= plugin.Run
                except:
                    print("Ignored >> Load {} Fail.".format(module_name))
                    continue
            bvb = Gtk.VBox(spacing=1)
            
            b = Gtk.Button(always_show_image=True,relief=Gtk.ReliefStyle.NONE)
            if mainbuttonbold:
                bl = Gtk.Label("<b>"+button_label+"</b>",use_markup=True)
            else:
                bl = Gtk.Label(button_label)
            bl.set_line_wrap(True)
            bl.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
            bl.set_max_width_chars(14)
            bl.set_justify(Gtk.Justification.CENTER)
            if mainbuttontooltip:
                b.set_tooltip_markup(mainbuttontooltip)
            b.set_size_request(mainbuttonsizewidth,mainbuttonsizeheight)
            if priority==1:
                b.connect("clicked",self.on_button_clicked2,plg,blockclose)
            elif priority>1:
                b.connect("clicked",run_function)
            else:
                b.connect("clicked",self.on_button_clicked,module_name,blockclose)
            bvb.pack_start(image,False,False,0)
            bvb.pack_start(bl,False,False,0)
            b.add(bvb)

            if len(all_category[category][0].get_children())==maxwidgetinrow:
                all_category[category][0] = Gtk.HBox(spacing=13)
                all_category[category][1].pack_end(all_category[category][0],False,False,0)

            h2categorybox.pack_start(b,False,False,10)
            
            
    
        self.show_all()

    def on_button_clicked2(self,button,plugin,blockclose):
        self.row.remove(self.maincontainer)
        if blockclose:
            self.header.set_show_close_button(False)
        backbutton = Gtk.Button()
        backbutton.connect("clicked",self.on_backbutton_clicked,plugin,blockclose)
        backbutton.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.headerhbox.add(backbutton)

        plugin.run()
        self.show_all()
        
        
    def on_button_clicked(self,button,module_name,blockclose):
        try:
            module = plugins_loader.load_plugin(module_name)
            plugin= module.Plugin(self,self.row)
        except Exception as e :
            print(e)
            print("Ignored >> Load {} Fail.".format(module_name))
            return
        self.row.remove(self.maincontainer)
        if blockclose:
            self.header.set_show_close_button(False)
        backbutton = Gtk.Button()
        backbutton.connect("clicked",self.on_backbutton_clicked,plugin,blockclose)
        backbutton.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.headerhbox.add(backbutton)

        plugin.run()
        self.show_all()
    
    def on_backbutton_clicked(self,button,plugin,blockclose):
        if blockclose:
            self.header.set_show_close_button(True)
        self.headerhbox.remove(button)
        button.destroy()
        plugin.stop()
        self.row.add(self.maincontainer)
        #self.show_all()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id=appid,
                         flags=Gio.ApplicationFlags.FLAGS_NONE,
                         **kwargs)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)
        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title=appwindowtitle)

        self.window.present()

    def on_quit(self, action, param):
        self.quit()

    def on_about(self,a,p):
        about = Gtk.AboutDialog(parent=self.window,transient_for=self.window, modal=True)
        about.set_program_name(appwindowtitle)
        about.set_version(version_)
        about.set_copyright(copyright_)
        about.set_comments(comments_)
        about.set_website(website_)
        #logo_=GdkPixbuf.Pixbuf.new_from_file(icon_)
        #about.set_logo(GdkPixbuf.Pixbuf.new_from_file(logo_))
        about.set_authors(authors_)
        about.set_license_type(Gtk.License.GPL_3_0)
        if translators_ != "translator-credits":
            about.set_translator_credits(translators_)
        about.run()
        about.destroy()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
