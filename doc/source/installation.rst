.. _installation:

Installation
============

Stable Version
--------------

We recommend install python-ari with ``pip``. At the command line::

    $ pip install python-ari

Development (Unstable) Version
------------------------------

If you want to run the latest development version of python-ari you will need
to install git and clone the repo from GitHub::

    $ git clone https://github.com/kickstandproject/python-ari
    $ cd python-ari
    $ python setup.py develop

.. note::
    The ``master`` branch is volatile and is generally not recommended for
    production use.

Alternatively, you can also install from GitHub directly with ``pip``.::

    $ pip install -e https://github.com/kickstandproject/python-ari#egg=python-ari
