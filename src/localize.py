#!/usr/bin/env python

import sys 
import os 
import argparse
import time
import json
from sys import version_info
from Parser import Parser
from Listener import Listener
from Utils import Utils
from Connector import Connector
from watchdog.observers import Observer
from colorama import init, Fore, Back, Style

def get_configuration (args):
  configuration = Parser(args.config)

  # Make sure the watch directory has a trailing slash
  configuration.watch_dir = os.path.normpath(configuration.watch_dir) + os.sep

  return configuration

def command(configuration, reset):

  if reset == "local":
    utils.reset_local()
  elif reset == "remote":
    utils.reset_remote()
  else:

  
  return utils


# Handle any command line arguments
def parse_args():
  config_required = True
  config_file = os.getcwd() + "/localize.cfg"

  # Check to see if the default config file exists
  if os.path.isfile(config_file):
    config_required = False

  p = argparse.ArgumentParser(description='Localize v0.0.1')

  p.add_argument("-c", "--config", help="A configuration file must be present.", required=config_required)
  p.add_argument("-r", "--reset", help="Options for this argument are [local|remote].", required=False)
  args = p.parse_args()

  # Add the default config to the args list
  if not config_required:
    args.config = config_file

  # If the reset option was passed 
  if args.reset and not args.reset in ("local", "remote"):
    p.error('Options for [-r RESET] are [local|remote].')
  
  return args

def main():
  # the call to init() will start filtering ANSI escape sequences out of any text sent to 
  # stdout or stderr, and will replace them with equivalent Win32 calls.
  init(autoreset=True)

  args = parse_args()
  configuration = get_configuration(args)

  # Run any start up utilities that were passed in on the command line
  command(configuration, args.reset)

if __name__ == '__main__': 
  main()
