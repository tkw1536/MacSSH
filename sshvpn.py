#!/usr/bin/env python

from subprocess import call, Popen
import sys

print(sys.argv)

if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    print("Usage: %s URI [IFACE]" % (sys.argv[0], ))
    sys.exit(1)

if len(sys.argv) > 2:
    iface = sys.argv[2]
else:
    iface = "Wi-Fi"

port = 2021
command = 'echo "Proxy connection established. " && read -n 1'

# COnfigure proxy
print("Configuring proxy URI ...")
call(["sudo", "networksetup", "-setsocksfirewallproxy", iface, "localhost", str(port), "off"])

# Connect
print("Establishing connection ...")
ssh_call = Popen(["ssh", "-D", str(port), host, command])

try:
    print("Press CTRL-C to disconnect. ")
    ssh_call.wait()
except KeyboardInterrupt:
    ssh_call.kill()
    

# Configure
print("Enabling proxy ...")
call(["sudo", "networksetup", "-setsocksfirewallproxystate", iface, "on"])

# And disable the proxy state
call(["sudo", "networksetup", "-setsocksfirewallproxystate", iface, "off"])