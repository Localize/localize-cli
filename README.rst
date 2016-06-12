localize-cli
=========

This package provides a unified command line interface to Localize.

Platforms
---------

- Mac OS X
- Windows
- Linux

------------
Installation
------------

The easiest way to install localize-cli is to use `pip`_::

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
also just `download the tarball`_.  Once you have the
localize directory structure on your workstation, you can just run::

    $ cd <path_to_localize>
    $ python setup.py install

Configuration
-------------

See the wiki_ for an example config file and configuration_ examples.

Usage
-----

See the wiki_ for examples on how to `get started`_ and other notes on usage_.
