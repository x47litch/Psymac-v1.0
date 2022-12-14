#!/bin/python3
import subprocess
import string
import random
import re
import pyfiglet;
import time
import argparse
from colorama import Fore,init
from Libs.landing import *

init();
def HeaderScript() :
    title = pyfiglet.figlet_format(f'{" "*2}psymac v1.0',font='slant');
    Banner = f'Github : {Fore.RED}x47litch{Fore.RESET} | Author : {Fore.RED}x47litch{Fore.RESET} | Copyright © {Fore.YELLOW}2022{Fore.RESET}';
    print(title);
    print('-'*68);
    print(' '*11,Banner);
    print('-'*68);

def get_random_mac_address():
    """Generate and return a MAC address in the format of Linux"""
    # get the hexdigits uppercased
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    # 2nd character must be 0, 2, 4, 6, 8, A, C, or E
    mac = ""
    for i in range(6):
        for j in range(2):
            if i == 0:
                mac += random.choice("02468ACE")
            else:
                mac += random.choice(uppercased_hexdigits)
        mac += ":"
    return mac.strip(":")


def get_current_mac_address(iface):
    # use the ifconfig command to get the interface details, including the MAC address
    output = subprocess.check_output(f"ifconfig {iface}", shell=True).decode()
    return re.search("ether (.+) ", output).group().split()[1].strip()


def change_mac_address(iface, new_mac_address):
    # disable the network interface
    subprocess.check_output(f"ifconfig {iface} down", shell=True)
    # change the MAC
    subprocess.check_output(f"ifconfig {iface} hw ether {new_mac_address}", shell=True)
    # enable the network interface again
    subprocess.check_output(f"ifconfig {iface} up", shell=True)

def handler(signum, frame):
        res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
        if res == 'y':
            exit(1)

if __name__ == "__main__":
    HeaderScript()
    parser = argparse.ArgumentParser(description="Python Mac Changer on Linux")
    parser.add_argument("interface", help="The network interface name on Linux")
    parser.add_argument("-r", "--random", action="store_true", help="Whether to generate a random MAC address")
    parser.add_argument("-l","--loop", action="store_true", help="Whether to set script loop")
    parser.add_argument("-m", "--mac", help="The new MAC you want to change to")
    args = parser.parse_args()
    iface = args.interface;

    #signal.signal(signal.SIGINT, handler)

    match args.loop:
        case True : 
            while(True) :
                if args.random:
                    # if random parameter is set, generate a random MAC
                    new_mac_address = get_random_mac_address()
                elif args.mac:
                    # if mac is set, use it instead
                    new_mac_address = args.mac
                # get the current MAC address
                old_mac_address = get_current_mac_address(iface)
                # change the MAC address
                change_mac_address(iface, new_mac_address)
                # check if it's really changed
                new_mac_address = get_current_mac_address(iface)
                loader = Loader(f"Please waiting a few second....",f"{old_mac_address} ==> {new_mac_address}")
                time.sleep(5)
                loader.stop();

        case False :
            if args.random:
                # if random parameter is set, generate a random MAC
                new_mac_address = get_random_mac_address()
            elif args.mac:
                # if mac is set, use it instead
                new_mac_address = args.mac
                # get the current MAC address
                old_mac_address = get_current_mac_address(iface)
                # change the MAC address
                change_mac_address(iface, new_mac_address)
                # check if it's really changed
                new_mac_address = get_current_mac_address(iface)
                loader = Loader(f"Please waiting a few second....",f"{old_mac_address} ==> {new_mac_address}")
                time.sleep(2)
                loader.stop();