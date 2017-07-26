#!/usr/bin/python

import os
import commands
import platform
import re

# import module snippets
from ansible.module_utils.basic import *

site_result={'ansible_facts': {}}

def check_zabbix_conf(package_name):
    try:
        f1 = open('/etc/zabbix/zabbix_agentd.conf', 'r')
	for i in f1.readlines():
    	    m = re.search('^UserParameter=', i)
	    if m:
		site_result['ansible_facts'][package_name]["custom_conf"]="True"
		break
    finally:
        if 'custom_conf' not in site_result['ansible_facts'][package_name]:
	    site_result['ansible_facts'][package_name]["custom_conf"]="False"
	f1.close()

def site_facts(module):

    package_name = module.params['package']
    # add package_name dict type declaration
    site_result['ansible_facts'][package_name] = {}

    if (package_name == "zabbix_scripts"):
        check_zabbix_conf(package_name)
    package = package_name.replace('_', '-')   
    cmd = "yum list installed | grep " + package
    
    package_info = commands.getoutput(cmd)

    if len(package_info) > 0:
        site_result['ansible_facts'][package_name]["installed"]="True" 
    else:
        site_result['ansible_facts'][package_name]["installed"]="False" 

    return site_result
   
def main():

    module = AnsibleModule(
            argument_spec = dict(
            package=dict(default="mongo", required=False),
        ),
        supports_check_mode = False,
    )
    
    data = site_facts(module)
    module.exit_json(**data)

main()
