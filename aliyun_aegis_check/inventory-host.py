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
####################

import sys
import getpass
from commands import getoutput

#HOME_DIR = getoutput('echo ~')
INV_PATH =  '/home/dreamer.xiong/server_nc'
try:
    import json
except ImportError:
    import simplejson as json

nc_inv = {}

def Usage():
    print "Usage:  %s --list or host <hostname>" % sys.argv[0]
    sys.exit(1)

def parse_inv(inv_path):
    inv = open(inv_path, 'r') 
    for line in inv:
        if ( line != '' or line != '\n' ) and (line.startswith('#') == False):
            vars = line.split()
            host_info = {}
            host_info["ansible_ssh_host"] = vars[1].split('=')[1]
            host_info["ansible_ssh_port"] = vars[2].split('=')[1]
            nc_inv[vars[0]] = host_info


def get_srv_pass(hostname):
    """
    ncadmin@srv-name's password:
    """
    password = getpass.getpass("ncadmin@" + hostname + "'s password:")
    return password


def grouplist(groupname):
    srvs = {}
    srvs[groupname] = {
        'hosts' : []
    }
    for srv in nc_inv.keys():
        srvs[groupname]['hosts'].append(srv)
    print json.dumps(srvs, indent=4)

def hostinfo(hostname):
    vars = {}
    vars['ansible_ssh_host'] = nc_inv[hostname]['ansible_ssh_host']
    vars['ansible_ssh_port'] = nc_inv[hostname]['ansible_ssh_port']
    vars['ansible_ssh_user'] = 'ncadmin'
    vars['ansible_ssh_pass'] = get_srv_pass(hostname)
    print json.dumps(vars, indent=4)


if __name__ == "__main__":
    parse_inv(INV_PATH)
    if len(sys.argv) == 2 and (sys.argv[1] == '--list'):
        grouplist('servers')
    elif len(sys.argv) == 3 and (sys.argv[1] == '--host'):
        hostinfo(sys.argv[2])
    else:
        Usage()
