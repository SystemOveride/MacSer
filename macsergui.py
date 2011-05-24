#!/usr/bin/python

# -*- coding: utf-8 -*-
#
#       MacSer
#       
#       Copyright 2011 systemoveride <systemoveride@live.it>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


#BackBox Linux Team

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import os
import re
import sys


class MacSer:

	def __init__(self):
			
		self.gladefile = "guis5.glade"  
	        self.root = gtk.glade.XML(self.gladefile) 
	        self.w_main = self.root.get_widget("window1")
	        self.w_main.connect("destroy", gtk.main_quit)
		
		dic = { "on_button1_clicked_change_mac" : self.button1_clicked,
				 "combobox1_changed" : self.combobox1_changed,
				 "on_button2_clicked" : self.button2_clicked,
				 "on_button3_clicked" : self.button3_clicked,
				 "on_button4_clicked" : self.button4_clicked,
				"on_MainWindow_destroy" : gtk.main_quit }
		self.root.signal_autoconnect(dic)
		
		self.entry1 = self.root.get_widget("entry1")
		self.entry2 = self.root.get_widget("entry2")
		self.label = self.root.get_widget('mac')
		self.combobox1=self.root.get_widget("combobox1")

		self.ModeChose = gtk.ListStore(str)
		self.ModeChose.append([' '])
		self.ModeChose.append(['Random'])
		self.combobox1.set_model(self.ModeChose)
		
		self.active = self.combobox1.get_active()

		
		self.w_main.show_all()
		
		

	def button1_clicked(self, widget):
		
		self.interface = self.entry2.get_text()
		
		if self.entry1.get_property('visible') == True:
			self.mac = self.entry1.get_text()
			try:
				os.system("python macser.py -m "+self.mac+" -i "+self.interface)
				self.label.set_text("New MAC Address: "+self.mac)
			except:
				print "Error"
				exit(0)
			
		else:
			os.system("python macser.py -r -i "+self.interface)
			self.look = os.popen('cat /sys/class/net/eth0/address')
			self.label.set_text("New MAC Address: "+str(self.look.read()))
			
		

	def combobox1_changed(self, widget):
		self.active = self.combobox1.get_active()
		if self.active == 1:
			print self.active
			self.entry1.hide()
		elif self.active != 1:
			self.entry1.show()
		
			
	def button2_clicked(self, widget):
		gtk.main_quit()
			
			
	def button3_clicked(self, widget):
		self.about = gtk.AboutDialog()
		self.about = gtk.AboutDialog()
		self.about.set_program_name("MacSer")
		self.about.set_version("0.1")
		self.about.set_comments("MacSer Change you Mac Address")
		self.about.set_copyright("(System_Overide)")
		self.about.set_website("http://backbox.org")
		self.about.run()
		self.about.destroy()
		
	def button4_clicked(self, widget):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.textview1 = gtk.TextView()
		self.textbuffer = self.textview1.get_buffer()
		self.window.add(self.textview1)
		self.textview1.set_editable(False)

		
		self.db = sys.path[0]+'/mac-database.txt'
		self.hex = ['A','B','C','D','E','F','1','2','3','4','5','6','7','8','9','0']
		self.limit = [':','-'] 
		
		self.look = os.popen('cat /sys/class/net/eth0/address')
		self.mac = str(self.look.read()).upper()
		if self.mac[2] in self.limit and self.mac[5] in self.limit and len(self.mac) > 7:
			self.mac = self.mac[0:2]+self.mac[3:5]+self.mac[6:8]
			for x in self.mac:
				if x not in self.hex:
					sys.exit(0)
		self.mac = self.mac[0:2]+'-'+self.mac[2:4]+'-'+self.mac[4:6]
		
		try:
			self.file = open(self.db,'r').read()
		except:
			sys.exit('error opening '+self.db)
			
		self.file = self.file.split('\n\n')

		for i in self.file:
			if self.mac in i:
				self.textbuffer.set_text(i)
		

		self.window.show()
		self.textview1.show()
		

if __name__ == "__main__":
	macser = MacSer()
	gtk.main()

