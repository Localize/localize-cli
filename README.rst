localize-cli
============

.. image:: https://circleci.com/gh/Localize/localize-cli/tree/master.svg?style=svg
   :target: https://circleci.com/gh/Localize/localize-cli/tree/master
   :alt: Build Status

This package provides a unified command line interface to Localize.

Platforms
---------

- Mac OS X
- Windows
- Linux

------------
Installation
------------

The easiest way to install localize-cli is to use `pip`::

  $ pip install localize

or, if you are not installing in a ``virtualenv``::

  $ sudo pip install localize

If you have the localize-cli installed and want to upgrade to the latest version
you can run::

  $ pip install --upgrade localize

.. note::

  On OS X, if you see an error regarding the version of six that came with
  distutils in El Capitan, use the ``--ignore-installed option``::

    $ sudo pip install localize --ignore-installed six


This will install the localize package as well as all dependencies. You can
also just download the tarball`.  Once you have the
localize directory structure on your workstation, you can just run::

  $ cd <path_to_localize>
  $ python setup.py install

---------------
Getting Started
---------------

Before using cli, you need to tell it about your Localize credentials.

The quickest way to get started is to run the ``localize config`` command::

    $ localize config
    Localize project key: 2pHF0QgIm8P3q
    Localize API token: b27406467cd9a8dfbdc1a1c02883fd69

---------------
Usage
---------------

- Push all local translations to Localize

    $ localize push

The command line tool will look at the `push` attribute in the config file to match
local files with resources to upload to Localize. The file name needs to match the
language code and the extension must be the format. For example, if uploading French
translations in the `YAML` format the filename would be `fr.yaml`.

    push:
      sources:
      - file: /Users/chris/files/fr.yaml

- Pull all remote translations from Localize

    $ localize pull

This command will overwrite or create new files with the content downloaded from Localize.
