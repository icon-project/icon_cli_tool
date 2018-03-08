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

-  0.0.1


Getting started
===============

Installation
------------

1. Clone this repository.

2. Change the just cloned project directory.

3. Execute following scripts.

.. code:: shell

    $ python3 -m python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements
    $ icli help

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
                transfer  <to> <amount> <file path> -p <password> -f <fee> -d <decimal point=18>  | -n <network id: mainnet | testnet>

                IF YOU MISS --networkid, icli WILL USE MAINNET.



    positional arguments:
      command           wallet create, wallet show, asset list, transfer

    optional arguments:
      -h, --help        show this help message and exit
      -p PASSWORD       password
      -f FEE            transaction fee
      -d DECIMAL_POINT  decimal point
      -n NETWORK_ID     which network
