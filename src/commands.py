#!/usr/bin/env python

import sys
import yaml
import os 
import argparse
import time
import requests
import json

from colorama import init, Fore, Back, Style

def get_url(conf):
  if conf['api']['dev']:
    base_url='http://localhost:8086/v2.0/projects/'
  else:
    base_url='https://api.localizejs.com/v2.0/projects/'

  return base_url+conf['api']['project']+'/resources'

def push(conf):
  errors = []
  for source in conf['push']['sources']:
    url = get_url(conf)
    headers={ 'Authorization': 'Bearer ' + conf['api']['token'] }

    # Try and open the file
    try:
      file = open(source['file'], 'rb')
    except (IOError, OSError) as e:
      errors.append('Error: ' + str(e))
      break;

    content={ 'content': file }

    # Use the file extension to guess the language and format
    base=os.path.basename(source['file'])
    language=os.path.splitext(base)[0]
    format=os.path.splitext(base)[1]
    data={
      'language': language,
      'format': format.replace('.','').upper()
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
    sys.exit(Fore.GREEN + 'Successfully pushed ' + str(len(conf['push']['sources'])) + ' file(s) to Localize!' + Style.RESET_ALL)

def pull(conf):
  errors = []
  for target in conf['pull']['targets']:
    url = get_url(conf)
    headers={
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + conf['api']['token'] 
    }

    # Use the file extension to guess the language and format
    base=os.path.basename(target['file'])
    language=os.path.splitext(base)[0]
    format=os.path.splitext(base)[1]
    data={
      'language': language,
      'format': format.replace('.','').upper(),
      'filter': 'has-active-translations'
    }

    r = requests.get(url, headers=headers, verify=False, params=data, stream=True)

    if r.status_code != 200:
      message = 'Something went wrong. Please contact support.'
      res = json.loads(r.text)
      if res['meta']['error']['message']:
        message = res['meta']['error']['message'] + ' for file ' + target['file']

      errors.append(message)
    else:
      # Swap put the content of the file with the data
      with open(target['file'], 'wb') as file:
        for chunk in r.iter_content(chunk_size=1024): 
          if chunk: # filter out keep-alive new chunks
            file.write(chunk)

  # If there are any errors display them to the user
  if errors:
    for error in errors:
      print(Fore.RED+error+Style.RESET_ALL)
  else:
    sys.exit(Fore.GREEN + 'Successfully pulled ' + str(len(conf['pull']['targets'])) + ' file(s) to Localize!' + Style.RESET_ALL)
