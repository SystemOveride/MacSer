#!/usr/bin/python

# -*- coding: utf-8 -*-
#
#       MacSer
#       
#       Copyright 2011 Luca Gagliardi <system_overide@live.it> <http://systemoveride.net>
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


from optparse import OptionParser, OptionGroup
import os
import random
import time
import sys
import re

try:  
	import pygtk  
	pygtk.require("2.0")  
except:  
	pass  
try:  
	import gtk  
	import gtk.glade  
except:  
	print("GTK Not Availible")
	sys.exit(1)
	
class color:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def blue(word):
	return color.BLUE + word + color.END

def pink(word):
	return color.PINK + word + color.END
	
def green(word):
	return color.GREEN + word + color.END

def yellow(word):
	return color.YELLOW + word + color.END
	
def red(word):
	return color.RED + word + color.END

class Service():
    def __init__(self):
		pass

    def random(self):
		self.mac = [ 0x00, 0x16, 0x3e,  
		random.randint(0x00, 0x7f),  
		random.randint(0x00, 0xff),  
		random.randint(0x00, 0xff) ]  
		return ':'.join(map(lambda x: "%02x" % x, self.mac)) 
		
    def change(self,interface,mac):
		self.device(interface)
		self.macvalidate(mac)
		try:
			os.system("ifconfig "+interface+" down")
			print green("[i] Interface "+interface+" down")
			time.sleep(3)
			os.system("ifconfig "+interface+" hw ether "+mac)
			print green("[i] Change MAC Address")
			os.system("ifconfig "+interface+" up")
			print green("[i] Interface "+interface+" up, restarting network-manager ...")
			time.sleep(3)
			os.popen("sudo service network-manager restart")
			print green("[i] New MAC Address: \033[1;33m"+mac+"\033[1;m")
			print green("Done")
		except:
			print red("[X] Error")
			exit(0)
			

    def findmac(self,interface):
		self.device(interface)
		
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
			sys.exit(read("[X] error opening "+self.db))
			
		self.file = self.file.split('\n\n')
		

		for i in self.file:
			if self.mac in i:
				self.look = os.popen('cat /sys/class/net/eth0/address')
				print "\n"+str(self.look.read())
				return sys.exit('\n'+i+'\n')
		print red("[!] Mac Not Found")
		sys.exit(0)
		
		
    def macvalidate(self,mac):
		self.regex = '([a-fA-F0-9]{2}[:|\-]?){6}'
		if not re.match(self.regex, mac) :
			print red(mac+" Is not a valid MAC Address")
			sys.exit(0)
		
		
    def device(self,interface):
		self.lt = []
		
		for i in os.listdir('/sys/class/net/'):
			self.lt.append(i)
			
		for y in self.lt:
			if not interface in self.lt:
				print red("[!] No interface "+interface+" found")
				sys.exit(0)

class MacSer(Service):

	def __init__(self):
			self.gladefile = "graphic.glade"  
			self.root = gtk.glade.XML(self.gladefile) 
			self.w_main = self.root.get_widget("window1")
			self.w_main.connect("destroy", gtk.main_quit)
			
			dic = { "on_MacChangeButton_clicked" : self.macchangebuttons_clicked,
					"on_ChoseBox_changed" : self.choseboxs_changed,
					"on_GetInformationButton_clicked" : self.getinformationbuttons_clicked,
					"on_UpdateButton_clicked" : self.updatebuttons_clicked,
					"on_CreditsButton_clicked" : self.creditsbuttons_clicked,
					"on_QuitButton_clicked" : self.quitbuttons_clicked,
					"on_MainWindow_destroy" : gtk.main_quit }
			self.root.signal_autoconnect(dic)
		
			self.eInterface = self.root.get_widget("InterfaceEntry")
			self.eMac = self.root.get_widget("MacEntry")
			self.lMacoutput = self.root.get_widget('MacOutputLabel')
			self.cChosebox=self.root.get_widget("ChoseBox")
		
			self.w_main.show_all()
		

	def macchangebuttons_clicked(self, widget):
		
		self.interface = self.eInterface.get_text()
		
		self.gdevice(self.interface)
		
		if self.eMac.get_property('visible') == True:
			self.mac = self.eMac.get_text()
			self.gmacvalidate(self.mac)
			try:
				self.change(self.interface,self.mac)
				self.lMacoutput.set_text("New MAC Address: "+self.mac)
			except:
				self.lMacoutput.set_text("Error")
				exit(0)
			
		else:
			self.mac = self.random()
			self.change(self.interface,self.mac)
			self.look = os.popen('cat /sys/class/net/'+self.interface+'/address')
			self.lMacoutput.set_text("New MAC Address: "+str(self.look.read()))
			
		

	def choseboxs_changed(self, widget):
		self.active = self.cChosebox.get_active()
		if self.active == 1:
			print self.active
			self.eMac.hide()
		elif self.active != 1:
			self.eMac.show()
			
		
	def getinformationbuttons_clicked(self, widget):
							
		self.interface = self.eInterface.get_text()
		
		self.gdevice(self.interface)
		
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.textview1 = gtk.TextView()
		self.textbuffer = self.textview1.get_buffer()
		self.window.add(self.textview1)
		self.textview1.set_editable(False)

		
		self.db = sys.path[0]+'/mac-database.txt'
		self.hex = ['A','B','C','D','E','F','1','2','3','4','5','6','7','8','9','0']
		self.limit = [':','-'] 
		
		self.look = os.popen('cat /sys/class/net/'+self.interface+'/address')
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
			self.textbuffer.set_text("Error opening "+self.db)
			
		self.file = self.file.split('\n\n')

		for i in self.file:
			if self.mac in i:
				self.textbuffer.set_text(i)
		

		self.window.show()
		self.textview1.show()
		
	def updatebuttons_clicked(self, widget):
		os.system("wget -O mac-database.txt http://standards.ieee.org/regauth/oui/oui.txt")
		self.lMacoutput.set_text("Mac database updated !")
		
	def gdevice(self,interface):
		self.lt = []
		
		for i in os.listdir('/sys/class/net/'):
			self.lt.append(i)
			
		for y in self.lt:
			if not interface in self.lt:
				self.dialog = gtk.MessageDialog(parent=None,flags=0, type=gtk.MESSAGE_ERROR,buttons=gtk.BUTTONS_OK,message_format="Interface not found")
				self.dialog.run()
				self.dialog.set_default_response(gtk.RESPONSE_OK)
				self.dialog.connect('response', self.dialog.destroy())
				
	def gmacvalidate(self,mac):
		self.regex = '([a-fA-F0-9]{2}[:|\-]?){6}'
		if not re.match(self.regex, mac) :
			self.dialog = gtk.MessageDialog(parent=None,flags=0, type=gtk.MESSAGE_ERROR,buttons=gtk.BUTTONS_OK,message_format="The mac address entered is notvalid")
			self.dialog.run()
			self.dialog.set_default_response(gtk.RESPONSE_OK)
			self.dialog.connect('response', self.dialog.destroy())
			sys.exit(0)
			
			
	def creditsbuttons_clicked(self, widget):
		self.about = gtk.AboutDialog()
		self.about = gtk.AboutDialog()
		self.about.set_program_name("MacSer")
		self.about.set_version("1.2")
		self.about.set_comments("MacSer Change your Mac Address")
		self.about.set_copyright("(System_Overide)")
		self.about.set_website("http://systemoveride.net")
		self.about.run()
		self.about.destroy()
		
	def quitbuttons_clicked(self, widget):
		gtk.main_quit()
		
		
parser = OptionParser( usage = "usage: %prog [options]" )

parser.add_option( "-r", "--random", action="store_true", dest="random", default=False, help="Generate random MAC Address ." );
parser.add_option( "-m", "--mac", action="store", dest="specific", default=None, help="Specific MAC Address ." );
parser.add_option( "-o", "--info", action="store_true", dest="info", default=None, help="Mac address INFO ." );
parser.add_option( "-i", "--interface", action="store", dest="interface", default=None, help="Internet Interface ." );
parser.add_option( "-g", "--gtk", action="store_true", dest="gtk", default=None, help="Run with GUI ." );


(o,args) = parser.parse_args()

Service = Service()

if not os.geteuid() == 0:
    print red("[!] Run this script with SUDO or root user\n")
    sys.exit(0)

if o.random == True:
	if o.interface != None:
		mac = Service.random()
		Service.change(o.interface,mac)
	else:
		print red("[!] Specific your Internet Interface\n")

elif o.specific:
	if o.interface == None:
		print red("[!] Specific your Internet Interface")
	else:
		Service.change(o.interface,o.specific)
			
elif o.info:
	if o.interface == None:
		print red("[!] Specific your Internet Interface")
		sys.exit(0)
	else:
		Service.findmac(o.interface)
		
elif o.gtk:
	macser = MacSer()
	gtk.main()

else:
	print parser.print_help()


