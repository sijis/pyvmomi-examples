from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import getpass
import vmutils

si = None
username = raw_input('Username: ')
password = getpass.getpass(prompt='Password: ')
vcenter = raw_input('vcenter: ')

try:
    si = SmartConnect(host=vcenter, user=username, pwd=password, port=443)
except IOError, e:
    pass

# Finding source VM
newvm = raw_input('New vm name: ')
template_vm = vmutils.get_vm_by_name(si, 'centos-6.5-x64')

'''
There are two roads for modifying a vm creation from a template
1. ConfigSpec -> CloneSpec
2. ConfigSpec -> (AdapterMapping -> GlobalIPSettings -> LinuxPrep) -> CustomSpec -> CloneSpec
Notes: 
    ConfigSpec and CustomSpecificiation are purely optional and
    independent
'''

# cpu/ram changes
#mem = 512 * 1024 # convert to GB
mem = 512  # MB
vmconf = vim.vm.ConfigSpec(numCPUs=1, memoryMB=mem)
#vmconf.deviceChange = devices

# Network adapter settings
adaptermap = vim.vm.customization.AdapterMapping()
adaptermap.adapter = vim.vm.customization.IPSettings(ip=vim.vm.customization.DhcpIpGenerator(), dnsDomain='domain.local')
# static ip
#adaptermap.adapter = vim.vm.customization.IPSettings(ip=vim.vm.customization.FixedIp(address='10.0.1.10'),
#                                                     subnetMask='255.255.255.0', gateway='10.0.0.1')

# IP
globalip = vim.vm.customization.GlobalIPSettings()
# for static ip
#globalip = vim.vm.customization.GlobalIPSettings(dnsServerList=['10.0.1.4', '10.0.1.1'])

# Hostname settings
ident = vim.vm.customization.LinuxPrep(domain='domain.local', hostName=vim.vm.customization.FixedName(name=newvm))

# Putting all these pieces together in a custom spec
customspec = vim.vm.customization.Specification(nicSettingMap=[adaptermap], globalIPSettings=globalip, identity=ident)


# Creating relocate spec and clone spec
resource_pool = vmutils.get_resource_pool(si, 'DEV')
relocateSpec = vim.vm.RelocateSpec(pool=resource_pool)
#cloneSpec = vim.vm.CloneSpec(powerOn=True, template=False, location=relocateSpec, customization=customspec, config=vmconf)
cloneSpec = vim.vm.CloneSpec(powerOn=True, template=False, location=relocateSpec, customization=None, config=vmconf)

# Creating clone task
clone = template_vm.Clone(name=newvm, folder=template_vm.parent, spec=cloneSpec)

# close out connection
Disconnect(si)
