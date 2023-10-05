# Functions Network
## Description
Functions Network is a script that allows you to visualize the link between every functions of a C project. The better use of this script is to use it on a project norm with the 42 Norm.
## Installation
```bash
apt-get install python3
pip install -r requirements.txt
```
## Usage
```bash
python funtions_network.py <path to files or directories> ...
```
## Example
```bash
python funtions_network.py file1.c file2.c
```
![Simple network on a file](img/simple.png)
![Simple network on 2 files](img/double.png)
```bash
python funtions_network.py dir/
```
![Network on multiples files and directories](img/big.png)
## Credits
This script use the following librarie:
- [pyvis](https://pyvis.readthedocs.io/en/latest/)

Created by Valentin Lepiller as side projectof the 42 school.
Feel free to use it! :)