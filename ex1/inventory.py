#!/usr/bin/python3.8
__author__ = "Oscar Lopez (oscar.lopez@anuvu.com)"
__version__ = ": 1.0 "
__date__ = "10//5/21"
__copyright__ = "Copyright (c) 2021 OL"
__license__ = "Python"

#
# Basic script to connect to obtain the IOS Version of backbone elements
#
import re
import pexpect
 
def get_devices_list():
    
    devices_list = []
    file = open('devices', 'r')

    for line in file:
        devices_list.append( line.rstrip() )

    file.close()

    print("devices list:", devices_list)
    return devices_list

def connect(ip_address, username, password):
    
    print ("establishing telnet session:", ip_address, username, password)
    telnet_command = 'telnet ' + ip_address

    # Connect via telnet to device
    session = pexpect.spawn('telnet ' + ip_address, timeout=20)
    result = session.expect(['Username:', pexpect.TIMEOUT])

    # Enter the username, expect password prompt afterwards
    session.sendline(username)
    result = session.expect(['Password:', pexpect.TIMEOUT])

    session.sendline(password)
    result = session.expect(['>', pexpect.TIMEOUT])

    print("--- connected to: ", ip_address)
    return session

def get_version_info(session):
    session.sendline('show version | include Version')
    result = session.expect(['>', pexpect.TIMEOUT])
    version_output_lines = session.before.splitlines()
    version = list(str(version_output_lines[4]).split(","))
    host = re.sub('b|\'|\#', '',str(version_output_lines[8]))
    print("\n version ", version[2])
    print("\n hostname: ", host)
    oscar = input()
    return version

devices_list = get_devices_list()    # Get list of devices

version_file_out = open('version-info-out', 'w')

# Loop through all the devices in the devices list
for ip_address in devices_list:

    # Connect to the device via CLI and get version information
    session = connect(ip_address, 'oscarl', 'huemac86')
    device_version = get_version_info(session)

    session.close()  # Close the session

    version_file_out.write('IP: '+ip_address+'  Version: '+device_version+'\n')

# Done with all devices and writing the file, so close
version_file_out.close()

# Standard call to the main() function.
if __name__ == '__main__':
    devices_list = get_devices_list()    # Get list of devices
    version_file_out = open('version-info-out', 'w')

# Loop through all the devices in the devices list
    for ip_address in devices_list:
    # Connect to the device via CLI and get version information
        session = connect(ip_address, 'cisco', 'cisco')
        device_version = get_version_info(session)
        session.close()  # Close the session
        version_file_out.write('IP: '+ip_address+'  Version: '+device_version+'\n')
# Done with all devices and writing the file, so close
    version_file_out.close()


