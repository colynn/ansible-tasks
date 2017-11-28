#!/usr/bin/env python
#! -*- coding:utf-8 -*-
####################
# This script is use to deal with those servers without ldap.
# As ansible only ask for password one time for all the servers
# in the specific playbook, so this script will ask for password 
# for each server, and then generate a dynamic playbook.
# Note:
# Ansible will run this server (number of servers + 1) times
# first time , get all the servers:
# python this_script.py --list
# other time, get all the servers' info:
# python this_script.py --host <hostname>
####################
####################
# Version 0.1 Jerry Jiang May 27 2015
# Version 0.2 Colynn Liu  June 21 2015
# Version 0.3 Dreamer Xiong July 27 2016
####################
import os
import sys
import getpass
import re
import commands

from ansible import errors

try:
    import json
except ImportError:
    import simplejson as json

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

nc_inv = OrderedDict() 
ldap_user = ""
ldap_pw = ""
#host_file = os.path.join(os.dirname(os.dirname(os.environ['PWD'])), "hosts")
bin_path = sys.path[0]
host_file = bin_path[:-3] + "hosts"

def Usage():
    print "Usage:  %s --list" % sys.argv[0]
    sys.exit(1)

if not os.path.exists(host_file):
    raise errors.AnsibleError("please put all hosts in the " + host_file + " file!")
    sys.exit(1)

def parse_hosts():
    origin = open(host_file, "r")
    servers = origin.readlines()
    server_list = servers
    nc_res = []
    un_res = open("unknown_servers", "w")
    config_str = commands.getoutput("""cat /etc/ssh/ssh_config |grep -v ^$| sed 's/^ *//g' | grep -v ^#""")
    for hostname in server_list:
        if hostname != "":
            if hostname.endswith("\n"):
                hostname = hostname.split()[0]
                m = re.search(r'host\s+' + hostname + r'\W*\nhostname\s+(?P<IP>\d+.\d+.\d+.\d+)+.*\nport\s+(?P<PORT>.*)', config_str)
                if m:
                    IP = m.group(1)
                    PORT = m.group(2).strip()
                    nc_res.append(
                                  hostname +
                                  " ansible_ssh_host=" +
                                  IP +
                                  " ansible_ssh_port=" +
                                  PORT 
                       )
                else:
                    un_res.write(hostname +  "\n")
    origin.close()
    un_res.close()
    if not nc_res:
        errors.AnsibleError("No hosts found!")
        sys.exit(1)
    if os.stat("unknown_servers").st_size == 0:
        os.remove("unknown_servers")
    return nc_res

def parse_inv(inv):
    ldap_hosts = 0
    for line in inv:
        if ( line != '' or line != '\n' ) and (line.startswith('#') == False):
            vars = line.split()
            host_info = {}
            host_info["ansible_ssh_host"] = vars[1].split('=')[1]
            host_info["ansible_ssh_port"] = vars[2].split('=')[1]
            nc_inv[vars[0]] = host_info
        if len(host_info["ansible_ssh_port"]) == 5 and host_info["ansible_ssh_port"].startswith('6'):
            ldap_hosts += 1
    return ldap_hosts

def get_srv_pass(hostname):
    """
    ncadmin@srv-name's password:
    """
    password = getpass.getpass("example-user@" + hostname + "'s password:")
    return password

def hostinfo(hostname):
    vars = {}
    vars['ansible_ssh_host'] = nc_inv[hostname]['ansible_ssh_host']
    vars['ansible_ssh_port'] = nc_inv[hostname]['ansible_ssh_port']
    if len(vars['ansible_ssh_port']) == 5 and vars['ansible_ssh_port'].startswith('6'):
        vars['ansible_ssh_user'] = ldap_user
        vars['ansible_ssh_pass'] = ldap_pw
    else:
        vars['ansible_ssh_user'] = 'example-user'
        vars['ansible_ssh_pass'] = get_srv_pass(hostname)
    return vars
    #print json.dumps(vars, indent=4)

def grouplist(groupname):
    srvs = {}
    srvs['_meta'] = {
        'hostvars':{}
    }
    srvs[groupname] = {
        'hosts' : []
    }
    for srv in nc_inv.keys():
        srvs[groupname]['hosts'].append(srv)
        vars = hostinfo(srv)
        srvs['_meta']['hostvars'][srv]=vars
    print json.dumps(srvs, indent=4)

if __name__ == "__main__":
    parsed_hosts = parse_hosts()
    ldap_hosts = parse_inv(parsed_hosts)
    if ldap_hosts > 0:
        ldap_user = getpass.getuser()
        ldap_pw = getpass.getpass(ldap_user + "@servers ldap's password: ")
    try: 
        grouplist('servers')
    except:
        Usage()
