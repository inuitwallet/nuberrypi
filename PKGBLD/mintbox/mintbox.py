#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sh
from colored import fore, style

def unlock_wallet():

	print
	print(fore.RED + style.BOLD + "WARNING! It is still not recommended to mint coins on NuBerryPi." + style.RESET)
	print(style.UNDERLINED + "This tool is here merely to enable faster testing." + style.RESET)
	print

	password = raw_input("Enter wallet password: ")

	try:
		sh.nud("walletpassphrase", password, "999999999", "true")
	except:
		print("Something went wrong")

if __name__ == "__main__":

	unlock_wallet()	
