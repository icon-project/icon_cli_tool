ICON CLI tool
=============

ICON supports Command Line Interface(CLI interface) for 3rd party or
user services development. With this single tool, you can control all
ICON functions and automate them using scripts.


Prerequisite
============

-  Python 3.6.x

Version
=======

-  0.0.3


Getting started
===============

Installation
------------

The easiest way to install ```icxcli``` is to use [pip](http://www.pip-installer.org/en/latest/):

```$ pip install icxcli```

or, if you are not installing in a virtualenv:

```$ sudo pip install icxcli ```

If you have the aws-cli installed and want to upgrade to the latest version you can run:

``` $ pip install --upgrade icxcli ```


Run CLI
-------

Run command icli in command line. There are many sub commands for ICX
service. You can get the help page by adding help.

.. code:: shell

$ icli  --help
    usage:
            Normal commands:
                version
                help

            Wallet Commands:
                wallet create <file path> -p <password>  | -n <network id: mainnet | testnet>
                wallet show <file path> -p <password>   | -n <network id: mainnet | testnet>
                asset list <file path> -p <password>    | -n <network id: mainnet | testnet>
                transfer  <to> <amount> <file path> -p <password> -f <fee>  | -n <network id: mainnet | testnet>

                IF YOU MISS --networkid, icli WILL USE TESTNET.



    positional arguments:
      command           wallet create, wallet show, asset list, transfer

    optional arguments:
      -h, --help        show this help message and exit
      -p PASSWORD       password
      -f FEE            transaction fee
      -n NETWORK_ID     which network
