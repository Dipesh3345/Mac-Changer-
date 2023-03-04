#!/usr/bin/env python3
import subprocess
import optparse
import re
import random

def banner():
    print("""                        ███╗   ███╗ █████╗  ██████╗     ██████╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ 
                        ████╗ ████║██╔══██╗██╔════╝    ██╔════╝██║  ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
                        ██╔████╔██║███████║██║         ██║     ███████║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
                        ██║╚██╔╝██║██╔══██║██║         ██║     ██╔══██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
                        ██║ ╚═╝ ██║██║  ██║╚██████╗    ╚██████╗██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
                        ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                            by Dipesh Dev                                              """)

def get_agruments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change Mac address")
   

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify a interface , use --help for more info")
    return options

def macgen():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


new_mac=macgen()

def mac_changer(interface, new_mac):
    print("[*] changing Mac address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    



def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    mac_address_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    

    if mac_address_search:
        return mac_address_search.group(0)
    else:
        print("[-]Couldn't found Mac address")



banner()
options = get_agruments()
current_mac = get_current_mac(options.interface)
print("Current mac of  "+ str(options.interface)+" is  "  + str(current_mac))
mac_changer(options.interface, new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == new_mac:
    print("[+] Mac address was sucessfully changed to " + current_mac +".")
else:
    print("[-] Mac address did not get chenged.")
