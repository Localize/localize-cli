#!/usr/bin/env python

import sys
import yaml
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # suppressing 'Unverified HTTPS request' msg
import json

from colorama import Fore, Style

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)       # suppressing 'Unverified HTTPS request' msg

def get_url(conf):
  if 'dev' in conf['api']:
    base_url='http://localhost:8086/v2.0/projects/'
  elif 'staging' in conf['api']:
    base_url='https://api.localizestaging.com/v2.0/projects/'
  else:
    base_url='https://api.localizejs.com/v2.0/projects/'

  return base_url+conf['api']['project']+'/resources'

def config():
  project = input('Localize project key [None]: ')
  token = input('Localize API token [None]: ')

  data = dict(
    api = dict(
      project = project,
      token = token
    ),
    format = 'format',
    type = 'phrase',
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

def push(conf, profile):
  errors = []
  skip = 0

  if profile and not profile in conf['push']:
    sys.exit(Fore.RED + 'Could not find matching config. Please make sure you specified the right name in --config.' + Style.RESET_ALL)

  if profile and not 'sources' in conf['push'][profile]:
    sys.exit(Fore.RED + 'Could not find any sources to push in the config set. Please make sure your configuration is formed correctly.' + Style.RESET_ALL)

  if not 'sources' in conf['push']:
    sys.exit(Fore.RED + 'Could not find any sources to push. Please make sure your configuration is formed correctly.' + Style.RESET_ALL)

  # Assume pushing phrases unless specified in config_file
  if profile and 'type' in conf['push'][profile]:
    type = conf['push'][profile]['type']
  elif 'type' in conf:
    type = conf['type']
  else:
    type = 'phrase'

  if profile and 'sources' in conf['push'][profile]:
    sourceFiles = conf['push'][profile]['sources']
  else:
    sourceFiles = conf['push']['sources']

  for source in sourceFiles:
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
      print(Fore.RED + 'Skipping import of ' + language + '. No target file path in the localize cli config.yml' + Style.RESET_ALL)
      continue

    content={ 'content': file }

    data={
      'language': language,
      'type': type,
      'origin': 'cli',
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
    print(Fore.GREEN + 'Successfully pushed ' + str(len(conf['push']['sources'])-skip) + ' file(s) to Localize!' + Style.RESET_ALL)

def pull(conf, profile):
  errors = []
  if profile and not profile in conf['pull']:
    sys.exit(Fore.RED + 'Could not find matching config. Please make sure you specified the right name in --config.' + Style.RESET_ALL)

  if profile and not 'targets' in conf['pull'][profile]:
    sys.exit(Fore.RED + 'Could not find any targets to pull in the config set. Please make sure your configuration is formed correctly.' + Style.RESET_ALL)

  if not 'targets' in conf['pull']:
    sys.exit(Fore.RED + 'Could not find any targets to pull. Please make sure your configuration is formed correctly.' + Style.RESET_ALL)

  skip = 0

  # Assume pulling phrases unless specified in config_file
  if profile and 'type' in conf['pull'][profile]:
    type = conf['pull'][profile]['type']
  elif 'type' in conf:
    type = conf['type']
  else:
    type = 'phrase'

  if profile and 'targets' in conf['pull'][profile]:
    targetFiles = conf['pull'][profile]['targets']
  else:
    targetFiles = conf['pull']['targets']
  for target in targetFiles:
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

    file = list(target.values())[0]

    # Use the key as the language
    language =  list(target.keys())[0]

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
        print(Fore.RED + 'Skipping export of ' + language + '. No target file path in the localize cli config.yml' + Style.RESET_ALL)

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
