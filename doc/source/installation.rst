.. _installation:

Installation
============

Stable Version
--------------

We recommend install python-ari with ``pip``. At the command line::

    pip install python-ari

Development (Unstable) Version
------------------------------

.. note::

    This document originates from the OpenStack project. Since we also use the
    same toolset for testing, we can also use some of their documentaion. We
    have obviously made changes that only affect our project but we credit the
    OpenStack project for the original [#f1]_.

If you want to run the latest development version of python-ari you will need
to install git and clone the repo from GitHub::

    git clone https://github.com/kickstandproject/python-ari
    cd python-ari

Installing and using the virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install the virtual environment you simply run the following::

    python tools/install_venv.py

This will install all of the Python packages listed in the
``requirements.txt`` file into your virtualenv. There will also be some
additional packages (pip, distribute, greenlet) that are installed by the
``tools/install_venv.py`` file into the virutalenv.

If all goes well, you should get a message something like this::

    Python-ari development environment setup is complete.

    Python-ari development uses virtualenv to track and manage Python
    dependencies while in development and testing.

    To activate the python-ari virtualenv for the extent of your current shell
    session you can run:

    $ source /home/pabelanger/git/pabelanger/python-ari/.venv/bin/activate

    Or, if you prefer, you can run commands in the virtualenv on a case by case
    basis by running:

    $ /home/pabelanger/git/pabelanger/python-ari/tools/with_venv.sh <your command>

    Also, make test will automatically use the virtualenv.

To activate the python-ari virtualenv for the extent of your current shell session you can run::

    source .venv/bin/activate

.. [#f1] See http://docs.openstack.org/developer/nova/devref/development.environment.html
