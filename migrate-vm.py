from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import getpass
import vmutils
import random

si = None
username = raw_input('Username: ')
password = getpass.getpass(prompt='Password: ')
vcenter = raw_input('vcenter: ')
vm_name = raw_input('VM: ')
esx_host = raw_input('ESX Host: ')

try:
    si = SmartConnect(host=vcenter, user=username, pwd=password, port=443)
except IOError, e:
    pass

if esx_host == '':
    all_hosts = vmutils.get_hosts(si)
    esx_host = vmutils.get_host_by_name(si, random.choice(all_hosts.values()))
else:
    esx_host = vmutils.get_host_by_name(si, esx_host)

# Finding source VM
vm = vmutils.get_vm_by_name(si, vm_name)

# relocate spec, to migrate to another host
# this can do other things, like storage and resource pool
# migrations
relocate_spec = vim.vm.RelocateSpec(host=esx_host)

# does the actual migration to host
vm.Relocate(relocate_spec)

Disconnect(si)
