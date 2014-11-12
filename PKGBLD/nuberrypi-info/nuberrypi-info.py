#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Copyright 2014 Peerchemist
#
# This file is part of NuBerryPi project.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
 
__author__ = "Peerchemist"
__license__ = "GPL"
__version__ = "0.23"

import os, sys
import sh
import argparse
import json
import urllib
import platform
from datetime import timedelta
from datetime import datetime as dt
from colored import fore, back, style

## Class that pulls and parses data
class pbinfo:

	def system(self):

		def uptime():

			with open('/proc/uptime', 'r') as f:
				uptime_seconds = float(f.readline().split()[0])
				uptime_str = str(timedelta(seconds = uptime_seconds))

			return(uptime_str)

		def distr():

			with open('/etc/os-release', 'r') as lsb:
				for line in lsb:
					if line.startswith('VERSION_ID'):
						return(line.split('=')[1].replace('"','').strip())

		def temp():

			with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp:
				return(float(temp.readline().strip())/1000)

		mm = {
			'nuberrypi': distr(),
			'kernel release': platform.release(),	
			'uptime': uptime(),
			'average load': os.getloadavg(),
			'system_temperature': temp()
			}

		return(mm)


	def hardware(self):

		mm = {}

		with open('/proc/cpuinfo') as cpuinfo:
			for line in cpuinfo:
				if line.startswith('Hardware'):
					hardware = line.split(':')[1].strip()
					if hardware == "BCM2708":
						mm['hardware'] = "Raspberry Pi"

				if line.startswith('Serial'):
					ser = line.split(':')[1].strip()
					mm['serial'] = ser


		with open('/proc/cmdline', 'r') as cmdline:
			for i in cmdline.readline().split():
				if i.startswith('smsc95xx.macaddr'):
					mm['maccaddr'] = str(i.split('=')[1])

				if i.startswith('bcm2708.boardrev'):
					mm['board_rev'] = str(i.split('=')[1])

		return(mm)


	def nud(self, argv):

		get = sh.nud("getinfo", _ok_code=[0,3,5,87]).stdout
		pos_diff = sh.nud("getdifficulty", _ok_code=[0,3,5,87]).stdout

		try:
			getinfo = json.loads(get)
			pos = json.loads(pos_diff)['proof-of-stake']
			getinfo["difficulty proof-of-stake"] = pos
		except:
			return("nud inactive")

		## When posting in public, hide IP and balance.
		if argv == "private":
			del getinfo['balance']
			del getinfo['ip']
			return(getinfo)

		else:
			return(getinfo)

## Class that will do all the pretty printing
class box:

	def default(self): ## printed when no arguments

		box = {}
		box['nuberrypi version'] = "v" + pbinfo.system()['nuberrypi']
		box['uptime'] = pbinfo.system()['uptime']
		box['nud'] = pbinfo.nud(self)
		box['serial'] = pbinfo.hardware()['serial']
		box['raspi_board_rev'] = pbinfo.hardware()['board_rev']

		print(fore.GREEN + style.UNDERLINED + "NuBerryPi:" + style.RESET)
		print(json.dumps(box, sort_keys=True, indent=4))

		if box['nud'] == "nud inactive":
			print(fore.RED + style.BOLD + "WARNING: nud is not running!" + style.RESET)

	def public(self): ## When privacy is needed

		box = {}
		box['NuBerryPi:'] = "v" + pbinfo.system()['nuberrypi']
		box['serial'] = pbinfo.hardware()['serial']
		box['uptime'] = pbinfo.system()['uptime']
		box['nud'] = pbinfo.nud('private')
		print(fore.GREEN + style.UNDERLINED + "NuBerryPi:" + style.RESET)
		print(json.dumps(box, sort_keys=True, indent=4))		

	def system(self):

		box = pbinfo.system()
		print(fore.GREEN + style.UNDERLINED + "NuBerryPi system info:" + style.RESET)
		print(json.dumps(box, sort_keys=True, indent=4))

		if box['system_temperature'] > 76:
			print(fore.RED + style.BOLD + "WARNING: system temperature too high!" + style.RESET)

	def all(self): ## Switch to show all

		box = {}
		box['system'] = pbinfo.system()
		box['system'].update(pbinfo.hardware())
		box['nud'] = pbinfo.nud(self)
		print(json.dumps(box, sort_keys=True, indent=4))

	def health(self):

		report = health.check()
		print "Checking if we are on the right chain..."
		print "Using" + " " + style.UNDERLINED + "www.peerchain.co" + style.RESET + " as reference."
		print

		for k,v in report.items():
			if v == True:
				print(k + ":" + fore.GREEN + style.BOLD + "True" + style.RESET)
			else:
				print(k + ":" + fore.RED + style.BOLD + "False" + style.RESET)

		print


## Checking health of blockchain
class health:

	def pull(self):
		url = "https://peerchain.co/api/v1/blockLatest/"
		response = urllib.urlopen(url)
		return(json.loads(response.read()))

	def local(self):
		
		local = {}
		local["heightInt"] = int(sh.nud("getblockcount", _ok_code=[0,3,5,87]).stdout)

		local["hash"] = sh.nud("getblockhash", local["heightInt"],
												_ok_code=[0,3,5,87]).stdout.strip()

		block_info = json.loads(sh.nud("getblock", local["hash"],
												_ok_code=[0,3,5,87]).stdout)

		local["prevHash"] = block_info["previousblockhash"]
		local["mrkRoot"] = block_info["merkleroot"]

		#timestring = block_info["time"].replace("UTC", "").strip()
		#local["timeStampUnix"] = dt.strptime(timestring
		#										, "%Y-%m-%d %H:%M:%S").strftime("%s")

		return local

	def check(self):

		local = self.local()
		remote = self.pull()
		report = {}

		if remote["heightInt"] == local["heightInt"]:
			report["block_count_matches"] = True
		else:
			report["block_count_matches"] = False

		if remote["hash"] == local["hash"]:
			report["last_block_hash_matches"] = True
		else:
			report["last_block_hash_matches"] = False

		if remote["prevHash"] == local["prevHash"]:
			report["previous_block_hash_matches"] = True
		else:
			report["previous_block_hash_matches"] = False

		if remote["mrkRoot"] == local["mrkRoot"]:
			report["merkle_root_matches"] = True
		else:
			report["merkle_root_matches"] = False

		return report


pbinfo = pbinfo()
box = box()
health = health()

######################### args

parser = argparse.ArgumentParser(description='Show information on NuBerryPi')
parser.add_argument('-a', '--all', help='show everything', action='store_true')
parser.add_argument('-s','--system', help='show system information', action='store_true')
parser.add_argument('-p', '--nu', help='equal to "ppcoid getinfo"', action='store_true')
parser.add_argument('--public', help='hide private data [ip, balance, serial]', action='store_true')
parser.add_argument('-o', '--output', help='dump data to stdout, use to pipe to some other program', 
																		action='store_true')
parser.add_argument('--health', help='compare local blockchain data with peerchain.co as reference',
																		action='store_true')
args = parser.parse_args()

## Default, if no arguments
if not any(vars(args).values()):
	box.default()

if args.all:
	box.all()

if args.system:
	box.system()

if args.nu:
	print(json.dumps(pbinfo.nud("self"), indent=4, sort_keys=True))

if args.public:
	box.public()

if args.output:
	sys.stdout.write(box.all())

if args.health:
	box.health()
