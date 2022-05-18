=======
idemenv
=======

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/


idemenv is an Idem binary installation and management tool, inspired by `tfenv <https://github.com/tfutils/tfenv>`__

About
=====

idemenv allows users to easily install multiple idem binaries built with tiamat.
This is useful for switching between idem configuration code bases written for
different idem versions.

idemenv is built as a POP application, which allows it to leverage other POP
plugins in the ecosystem or plug into other applications as necessary.

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.7+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``idemenv``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

      pip install idemenv

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@github.com/eitrtechnologies/idemenv.git
   cd idemenv

   # Setup venv
   python3 -m venv .venv --prompt idemenv
   source .venv/bin/activate
   pip install -e .

Usage
=====

.. code-block:: bash

   usage: run.py [-h] [--config CONFIG] [--config-template] [--log-datefmt LOG_DATEFMT] [--log-file LOG_FILE] [--log-fmt-console LOG_FMT_CONSOLE]
              [--log-fmt-logfile LOG_FMT_LOGFILE] [--log-handler-options [LOG_HANDLER_OPTIONS ...]] [--log-level LOG_LEVEL] [--log-plugin LOG_PLUGIN] [--repo-url REPO_URL]
              [--idemenv-dir SALTENV_DIR] [--version]
              {init,install,list,list-remote,pin,uninstall,use,version} ...

   positional arguments:
     {init,install,list,list-remote,pin,uninstall,use,version}

   options:
     -h, --help            show this help message and exit
     --config CONFIG, -c CONFIG
                           Load extra options from a configuration file onto hub.OPT.idemenv
     --config-template     Output a config template for this command
     --repo-url REPO_URL, -r REPO_URL
                           Idem single binary repository location. Version directories are expected here.
     --idemenv-dir IDEMENV_DIR, -d IDEMENV_DIR
                           Working directory for idemenv downloads
     --version             Display version information

   Logging Options:
     --log-datefmt LOG_DATEFMT
                           The date format to display in the logs
     --log-file LOG_FILE   The location of the log file
     --log-fmt-console LOG_FMT_CONSOLE
                           The log formatting used in the console
     --log-fmt-logfile LOG_FMT_LOGFILE
                           The format to be given to log file messages
     --log-handler-options [LOG_HANDLER_OPTIONS ...]
                           kwargs that should be passed to the logging handler used by the log_plugin
     --log-level LOG_LEVEL
                           Set the log level, either quiet, info, warning, debug or error
     --log-plugin LOG_PLUGIN
                           The logging plugin to use


Examples
--------

Basic idem binary setup:

.. code-block:: bash

   # Example CLI commands


   # List remote versions

   $ idemenv list-remote
   3004rc1
   3004
   3003.3
   3003


   # Install latest version

   $ idemenv install latest
   Processing tarball...


   # Use latest version

   $ idemenv use latest


   # List local versions

   $ idemenv list
   * 3004 set by /home/nmhughes/.idemenv/version
     3003.3
     3003


   # Initialize the idemenv environment, which will point to the idem binaries

   $ idemenv init
   Add the idemenv bin directory to your PATH:

       echo 'export PATH="$HOME/.idemenv/bin:$PATH"' >> ~/.bashrc
   OR:
       echo 'export PATH="$HOME/.idemenv/bin:$PATH"' >> ~/.zshrc

   $ echo 'export PATH="$HOME/.idemenv/bin:$PATH"' >> ~/.zshrc
   $ source ~/.zshrc


   # Kick the tires!

   $ idem exec test.version
   local:
       3004


Common Issues
=============

* If this error is encountered, you might be running on Arch and need to install the ``libxcrypt-compat`` package.

.. code-block:: text

    [230732] Error loading Python lib '/tmp/_MEIAEr7dd/libpython3.7m.so.1.0': dlopen: libcrypt.so.1: cannot open shared object file: No such file or directory


Roadmap
=======

Reference the `open issues <https://github.com/eitrtechnologies/idemenv/issues>`__
for a list of proposed features (and known issues).

Acknowledgements
================

* `Img Shields <https://shields.io>`__ for making repository badges easy.
