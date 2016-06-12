#!/usr/bin/env python

import sys
import yaml
import os 
import argparse
import time
from colorama import init, Fore, Back, Style
from commands import *

def get_configuration(args):
  with open(args.config, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

  return cfg

def command(args, opts):
  if args.command=='push':
    push(opts)
  elif args.command=='pull':
    pull(opts)

# Handle any command line arguments
def parse_args():
  config_required = True
  config_file = os.getcwd() + "/config.yml"

  # Check to see if the default config file exists
  if os.path.isfile(config_file):
    config_required = False

  p = argparse.ArgumentParser(description='Localize v0.0.1')
  p.add_argument('command', nargs='?', help='an integer for the accumulator')
  p.add_argument("-c", "--config", help="A configuration file must be present.", required=config_required)

  args = p.parse_args()

  # Add the default config to the args list
  if not config_required:
    args.config = config_file
  
  return args

def main():
  # the call to init() will start filtering ANSI escape sequences out of any text sent to 
  # stdout or stderr, and will replace them with equivalent Win32 calls.
  init(autoreset=True)

  args = parse_args()
  configuration = get_configuration(args)

  # Run the command
  command(args, configuration)

if __name__ == '__main__': 
  main()
