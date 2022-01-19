#!/usr/bin/env python
import subprocess
import optparse
import re


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
    parser.add_option("-m", "--mac", dest="new_mac", help="New mac to be changed ")

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify a interface , use --help for more info")

    elif not options.new_mac:
        parser.error("[-] Please specify a Mac address , use --help for more info")

    return options


def mac_changer(interface, new_mac):
    print("[*] changing Mac address for " + interface + " to" + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print("[*]Changing Mac address to " +new_mac )



def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search:
        return mac_address_search.group(0)
    else:
        print("[-]Couldn't found Mac address")



banner()
options = get_agruments()
current_mac = get_current_mac(options.interface)
print("Current mac is " + str(current_mac))
mac_changer(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Mac address was sucessfully changed to " + current_mac +".")
else:
    print("[-] Mac address did not get chenged.")