#!/usr/bin/env python

import sys
import yaml
import os
import argparse
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # suppressing 'Unverified HTTPS request' msg
import json

from colorama import Fore, Back, Style

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)       # suppressing 'Unverified HTTPS request' msg

def get_url(conf):
  if 'dev' in conf['api']:
    base_url='http://localhost:8086/v2.0/projects/'
  else:
    base_url='https://api.localizejs.com/v2.0/projects/'

  return base_url+conf['api']['project']+'/resources'

def config():
  project = raw_input('Localize project key [None]: ')
  token = raw_input('Localize API token [None]: ')

  data = dict(
    api = dict(
      project = project,
      token = token
    ),
    format = 'format',
    push = dict(
      sources = [dict(file = '/full/path/to/your/language_code.format_extension')]
    ),
    pull = dict(
      targets = [dict(language_code = '/full/path/to/your/file_name.extension')]
    )
  )

  from os.path import expanduser
  home = expanduser("~")
  config_file = home + '/.localize/config.yml'

  if not os.path.exists(os.path.dirname(config_file)):
    try:
      os.makedirs(os.path.dirname(config_file))
    except OSError as exc: # Guard against race condition
      if exc.errno != errno.EEXIST:
        raise
  with open(config_file, 'w+') as out:
    out.write(yaml.dump(data, default_flow_style=False))

def push(conf):
  errors = []
  skip = 0

  # Assume pushing phrases unless specified in config_file
  if 'type' in conf:
    type = conf['type']
  else:
    type = 'phrase'

  for source in conf['push']['sources']:
    url = get_url(conf)
    headers={ 'Authorization': 'Bearer ' + conf['api']['token'] }

    if 'format' in source:
      format = source['format']
    else:
      format = conf['format']

    # Use the file extension to guess the language
    base = os.path.basename(source['file'])
    language = check_and_return_lang_format(base, 'push')     # refactoring, extracting duplicate code into method

    # Try and open the file
    try:
      file = open(source['file'], 'rb')
    except (IOError, OSError):
      skip =+ 1
      print(Fore.RED + 'Skipping import of ' + language + '. No target file path in the localize cli config.yml')
      continue

    content={ 'content': file }

    data={
      'language': language,
      'type': type,
      'format': format.replace('yml','yaml').upper()  # replacing 'yml' file format to 'yaml'
    }

    r = requests.post(url, headers=headers, verify=False, data=data, files=content)

    if r.status_code != 200:
      message = 'Something went wrong. Please contact support.'
      res = json.loads(r.text)

      if res['meta']['error']['message']:
        message = res['meta']['error']['message'] + ' for file ' + source['file']

      errors.append(message)

  # If there are any errors display them to the user
  if errors:
    for error in errors:
      print(Fore.RED+error+Style.RESET_ALL)
  else:
    sys.exit(Fore.GREEN + 'Successfully pushed ' + str(len(conf['push']['sources'])-skip) + ' file(s) to Localize!' + Style.RESET_ALL)

def pull(conf):
  errors = []

  if not 'targets' in conf['pull']:
    sys.exit(Fore.RED + 'Could not find any targets to pull. Please make sure your configuration is formed correctly.' + Style.RESET_ALL)

  skip = 0

  # Assume pulling phrases unless specified in config_file
  if 'type' in conf:
    type = conf['type']
  else:
    type = 'phrase'

  for target in conf['pull']['targets']:
    if not target:
      sys.exit(Fore.RED + 'Could not find target.' + Style.RESET_ALL)

    url = get_url(conf)
    headers={
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + conf['api']['token']
    }

    if 'format' in target:
      format = target['format']
    else:
      format = conf['format']

    file = target.values()[0]

    # Use the key as the language
    language = target.keys()[0]

    data={
      'language': language,
      'type': type,
      'format': format.replace('yml','yaml').upper(),    # replacing 'yml' file format to 'yaml
      'filter': 'has-active-translations'
    }

    r = requests.get(url, headers=headers, verify=False, params=data, stream=True)

    if r.status_code != 200:
      message = 'Something went wrong. Please contact support.'
      res = json.loads(r.text)
      if res['meta']['error']['message']:
        message = res['meta']['error']['message'] + ' for file ' + file
        skip =+ 1

      errors.append(message)
    else:
      # Swap put the content of the file with the data
      try:
        with open(file, 'wb') as file:
          for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
              file.write(chunk)
      except IOError:
        skip =+ 1
        print(Fore.RED + 'Skipping export of ' + language + '. No target file path in the localize cli config.yml')

  # If there are any errors display them to the user
  if errors:
    for error in errors:
      print(Fore.RED + error + Style.RESET_ALL)
  else:
    sys.exit(Fore.GREEN + 'Successfully pulled ' + str(len(conf['pull']['targets'])-skip) + ' file(s) from Localize!' + Style.RESET_ALL)

def check_and_return_lang_format(filename, type):
  if filename.count('.') != 1:                      # checking filename, shoud be '<lang>.<format>', for example ru.json, es.csv
    sys.exit(Fore.RED + "Wrong filename for '" + type + "' type, target file have to has the following file format '<language>.<format>', for example ru.json" + Style.RESET_ALL)
  splitted_filename = filename.split('.')           # splitting filename by dot
  return splitted_filename[0]  # returning language
