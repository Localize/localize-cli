#!/usr/bin/env python

import sys
import yaml
import os 
import argparse
import time
import requests
import json

from colorama import init, Fore, Back, Style

def push(conf):
  errors = []
  for sources in conf['push']['sources']:
    if conf['api']['dev']:
      base_url='http://localhost:8086/v2.0/projects/'
    else:
      base_url='https://api.localizejs.com/v2.0/projects/'

    url = base_url+conf['api']['project']+'/resources'
    headers={ 
      'Authorization': 'Bearer ' + conf['api']['token']
    }

    # Use the file extension to guess the language and format
    base=os.path.basename(sources['file'])

    
    # Try and open the file
    try:
      file = open(sources['file'], 'rb')
    except (IOError, OSError) as e:
      errors.append('Error: ' + str(e))
      break;

    content={ 'content': file }

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
        message = res['meta']['error']['message'] + ' for file ' + sources['file']

      errors.append(message)
      # sys.exit(Fore.RED + message + ' for file ' + sources['file'] +Style.RESET_ALL)

  # If there are any errors dispaly them to the user
  if errors:
    for error in errors:
      print(Fore.RED+error+Style.RESET_ALL)
  else:
    sys.exit(Fore.GREEN + 'Successfully pushed ' + str(len(conf['push']['sources'])) + ' file(s) to Localize!' + Style.RESET_ALL)
