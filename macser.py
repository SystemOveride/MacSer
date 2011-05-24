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


from optparse import OptionParser, OptionGroup
import os
import random
import time
import sys


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
		print mac
		try:
			os.system("ifconfig "+interface+" down")
			print "@Interface "+interface+" down"
			time.sleep(3)
			os.system("ifconfig "+interface+" hw ether "+mac)
			print "@Change MAC Address"
			os.system("ifconfig "+interface+" up")
			print "@Interface "+interface+" up, restarting network-manager ..."
			time.sleep(3)
			os.system("sudo service network-manager restart")
			print "New MAC Address: \033[1;33m"+mac+"\033[1;m"
			print "Done"
		except:
			print "Error"
			exit(0)

    def findmac(self,interface):
		
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
				self.look = os.popen('cat /sys/class/net/eth0/address')
				print "\n"+str(self.look.read())
				sys.exit('\n'+i+'\n')
		print "Mac Not Found"
				

parser = OptionParser( usage = "usage: %prog [options]" )

parser.add_option( "-r", "--random", action="store_true", dest="random", default=False, help="Generate random MAC Address ." );
parser.add_option( "-m", "--mac", action="store", dest="specific", default=None, help="Specific MAC Address ." );
parser.add_option( "-o", "--info", action="store_true", dest="info", default=None, help="Mac address INFO ." );
parser.add_option( "-i", "--interface", action="store", dest="interface", default=None, help="Internet Interface ." );


(o,args) = parser.parse_args()

Service = Service()

if not os.geteuid()==0:
    print '\033[1;33mRun this sript with SUDO or root user\033[1;m'
    sys.exit(0)

if o.random == True:
	if o.interface != None:
		mac = Service.random()
		Service.change(o.interface,mac)
	else:
		print '\033[1;33mSpecific you Internet Interface\033[1;m'

elif o.specific:
	if o.interface == None:
		print '\033[1;33mSpecific you Internet Interface\033[1;m'
	else:
		Service.change(o.interface,o.specific)
			
elif o.info:
	if o.interface == None:
		print '\033[1;33mSpecific you Internet Interface\033[1;m'
	else:
		Service.findmac(o.interface)

else:
	print parser.print_help()

