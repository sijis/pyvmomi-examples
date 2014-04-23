from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import getpass
import vmutils

si = None
username = raw_input('Username: ')
password = getpass.getpass(prompt='Password: ')
vcenter = raw_input('vcenter: ')
vm_name = raw_input('VM: ')

try:
    si = SmartConnect(host=vcenter, user=username, pwd=password, port=443)
except IOError, e:
    pass

# Finding source VM
vm = vmutils.get_vm_by_name(si, vm_name)

# does the actual vm reboot
try:
    vm.RebootGuest()
except:
    # forceably shutoff/on
    # need to do if vmware guestadditions isn't running
    vm.ResetVM_Task()

Disconnect(si)
