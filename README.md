 ICON CLI tool
========

 ICON supports Command Line Interface(CLI interface) for 3rd party or user services development. With this single tool, you can control all ICON functions and automate them using scripts.

<!-- TOC depthFrom:1 depthTo:3 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Prerequisite](#prerequisite)
- [Version](#version)
- [Glossary](#glossary)
- [Technical information](#technical-information)
- [Getting started](#getting-started)
	- [Installation](#installation)
	- [Run CLI](#run-cli)
	- [Console instructions](#console-instructions)
	- [Wallet operation](#wallet-operation)
		- [Create wallet from file](#create-wallet-from-file)
		- [Show wallet information](#show-wallet-information)
		- [List up all assets in current wallet](#list-up-all-assets-in-current-wallet)
		- [Transfer the value to the specific address with the fee.](#transfer-the-value-to-the-specific-address-with-the-fee)

<!-- /TOC -->

# Prerequisite

* Python 3.6.x

# Version

* 0.01 beta

# Glossary

* Address of wallet: Unique string to identify the address to transfer value. It begins with hx.

* Private key: A tiny bit of code that is paired with a public key to set off algorithms to encrypt and decrypt a text  for the specific address.

* Public key: Long alphanumeric characters that is used to encrypt data (message).

# Technical information

There are five steps to get from  private->public -> address:

1. Generate a private key.

2. Derive a public key from the private key.

3. H1 = sha3_256( Public key)  => 32 byte

4. BitAddress = last 20 bytes of H1

5. Address = hx || HexString(BitAddress)
ex) hxaa688d74eb5f98b577883ca203535d2aa4f0838c

# Getting started

## Installation

1. Clone this repository.

2. Change the just cloned project directory.

3. Execute following scripts.

```shell
$ python3 -m python3 venv
$ source venv/bin/activate
$ pip install -r requirements
$ icli help
```

## Run CLI

 Run command icli in command line.  There are many sub commands for ICX service. You can get the help page by adding help.


```shell
$ icli help

Normal commands:
      version
      help

Wallet Commands:
      wallet create <file path> -p <password>
      wallet show <file path> -p <password>
      asset list <file path> -p <password>
      transfer  <to> <amount> <file path> -p <password> -f <fee> -d <decimal point=18>
```

## Console instructions

<table>
  <tr>
    <td>Command</td>
    <td>Function description</td>
  </tr>
  <tr>
    <td>version</td>
    <td>Shows the current software version. </td>
  </tr>
  <tr>
    <td>help</td>
    <td>Shows Help menu</td>
  </tr>
</table>


## Wallet operation

<table>
  <tr>
    <td>Command</td>
    <td>Function description</td>
  </tr>
  <tr>
    <td>wallet create <file path> -p <password>
      </td>
    <td>Create a wallet file.</td>
  </tr>
  <tr>
    <td>wallet show <file path> -p <password>
</td>
    <td>Show current wallet information.</td>
  </tr>
  <tr>
    <td>asset list <file path> -p <password>
      </td>
    <td>Enumerate the asset in the wallet. (ICX, ICX token) </td>
  </tr>
  <tr>
    <td>transfer  <to> <amount> <file path> -p <password> -f <fee> -d <decimal point=18>
</td>
    <td>Transfer the value to the specific address with the fee. </td>
  </tr>
</table>


### Create wallet from file

```shell
$ icli wallet create <wallet name> <file path> -p <password>
```

Create a wallet file with given wallet name, password and file path.

#### Arguments

* file path : File path for the keystore file of the wallet.

* password: Password including alphabet character, number, and  special character. If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.

#### Output

##### Successful case

Return 0 : Succeed to generate the keystore file for the wallet.

##### Error cases

icli will return following error code and message.

* Return 122: File path is wrong.

* Return 123: Password is wrong.

* Return 136: User does not have enough permission to write the file.

### Show wallet information

```shell
$ icli wallet show <file path> -p <password>
```

Show wallet information.

#### Arguments

* file path : File path for the keystore file of the wallet.

* password:  Password including alphabet character, number, and  special character. If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.

#### Output

Shows the all information of wallet.

##### Successful case

Return 0 : Print out wallet information including asset list.

##### Error cases

* Return 122: File path is wrong.

* Return 123: Password is wrong.

* Return 130: Wallet address is wrong.

### List up all assets in current wallet

```
$ icli asset list <file path> -p <password>
```

 Enumerate the list of all the assets of the wallet.

#### Arguments

* file path : File path for the keystore file of the wallet.

* password: Password including alphabet character, number, and  special character. If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.

#### Output

* List of all assets in current wallet.

##### Successful case

* Return 0 : Succeed to display.

##### Error cases

* Return 122: File path is wrong.

* Return 123: Password is wrong.

* Return 130: Wallet address is wrong.

### Transfer the value to the specific address with the fee.

```shell
$ icli transfer <to> <amount> <file path> -p <password> -f <fee> -d <decimal point=18>
```


Transfer the value from  A address to B address with the fee.

#### Arguments

* amount : Amount of money. **The decimal point number is valid up to tenth power of 18. **

* to: Address of wallet to receive the asset.

* fee : Transfer fee

* file path : File path for the keystore file of the wallet.

* password:  Password including alphabet character, number, and  special character. If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.

* decimal point :  A user can change the decimal point to express all numbers including fee and amount.

    * **YOU SHOULD CHANGE BOTH THE EXPRESSION OF AMOUNT AND THE EXPRESSION OF FEE IF ANY.**
    - Ex) Amount value  0.001 with default decimal point will be 0.001*10^12 = 10,000,000,000.0 with decimal point = 12.

#### Output

##### Successful case

Return 0 : Succeed to transfer

##### Error cases

icli will return following error code and message.

* Return 122: File path is wrong.

* Return 123: Password is wrong.

* Return 127: Wallet does not have enough balance.

* Return 128: Transfer fee is invalid.

* Return 129: Timestamp is not correct. (Reset your computer’s time and date.)

* Return 130: Wallet address is wrong.


# Development

Run ```icli``` in development as following.

```bash
$ python -m icxcli $commands $args...
``` 