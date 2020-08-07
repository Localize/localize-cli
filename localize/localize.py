#!/usr/bin/env python

import sys
import yaml
import os
import argparse
import time
from colorama import init, Fore, Back, Style
from commands import *

def get_configuration(args):
  from os.path import expanduser
  home = expanduser("~")
  config_file = home + '/.localize/config.yml'

  # Check to see if the config file exists
  if not os.path.isfile(config_file):
    print(Fore.RED + 'No configuration file found! Run the following command to create one:' + Style.RESET_ALL)
    print('')
    print('    localize config')
    print('')
    print('You can also create the file manually in your $HOME directory: $HOME/.localize/config.yml')
    print('')
    sys.exit()

  with open(config_file, 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

  return cfg

def command(args):
  # Load up the configuration or let the user know to run init
  if not args.command=='config':
    configuration = get_configuration(args)

  if args.command=='push':
    push(configuration)
  elif args.command=='pull':
    pull(configuration)
  elif args.command=='config':
    config()
  else:
    sys.exit(Fore.RED + 'Not a valid command! Did you mean config, push, or pull?' + Style.RESET_ALL)

# Handle any command line arguments
def parse_args():
  p = argparse.ArgumentParser(description='Localize')
  p.add_argument('command', nargs='?', help='an integer for the accumulator')

  args = p.parse_args()

  return args

def main():
  # the call to init() will start filtering ANSI escape sequences out of any text sent to
  # stdout or stderr, and will replace them with equivalent Win32 calls.
  init(autoreset=True)

  # Checks the command line arguments
  args = parse_args()

  # Run the command
  command(args)



if __name__ == '__main__':
  main()
