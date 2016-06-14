import sys
import getopt
from ConfigParser import SafeConfigParser
from colorama import Fore, Back, Style

sections = 'api', 'dir'

class Parser(object):
	def __init__(self, *file):
		parser = SafeConfigParser()
		parser.optionxform = str
		found = parser.read(file)
		if not found:
			sys.exit(Fore.RED + "No config file found!" + Style.RESET_ALL)
		for name in sections:
			self.__dict__.update(parser.items(name))