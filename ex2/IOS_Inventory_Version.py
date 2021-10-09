#!/usr/bin/python3.8
__author__ = "Oscar Lopez (oscar.lopez@anuvu.com)"
__version__ = ": 1.0 "
__date__ = "10//5/21"
__copyright__ = "Copyright (c) 2021 OL"
__license__ = "Python"

#
# Basic script to obtain IOS Version of backbone elements
#
import re
import pexpect
 
def get_devices_list():
    devices_list = []
    file = open('devices', 'r')
    for line in file:
        devices_list.append( line.rstrip() )
    file.close()
    print("\n Obtaining Software version of the following devices :", devices_list)
    return devices_list

def connect(ip_address, username, password):
    print ("establishing ssh session to: ", ip_address)
    session = pexpect.spawn('ssh ' + username + '@' + ip_address, timeout=20, encoding='utf-8')    
    result = session.expect(['Password:', pexpect.TIMEOUT])
    session.sendline(password)
    result = session.expect(['>', pexpect.TIMEOUT])
    print("\n Connected to: \n", ip_address)
    return session

def get_version_info(session):
    session.sendline('sh ver | inc Version')
    result = session.expect(['>', pexpect.TIMEOUT])
    version_output_lines = session.before.splitlines()
    print(version_output_lines)
    version = version_output_lines[3]
    host = re.sub('\#', '',str(version_output_lines[8]))
    return [host,version]

def main():
    devices_list = get_devices_list()  
    version_file_out = open('IOS-version-info.txt', 'w')
    version_file_out.write("Inventory of IOS XE Versions installed in Backbone Routers" "\n")
    version_file_out.write("--------------------------------------------------------------------------" "\n") 
    for ip_address in devices_list:
        session = connect(ip_address, 'oscarl', 'huemac86')
        device = get_version_info(session)
        session.close()  
        version_file_out.write("%s   %s   %s\n" % (device[0], ip_address, device[1]))
    version_file_out.write("--------------------------------------------------------------------------" "\n")    
    version_file_out.close()
    print("---------------------------------------")
    print("\n Inventory Created successfully!!!")
    print("---------------------------------------")
    
if __name__ == '__main__':
    main()

