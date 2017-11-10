#!/usr/bin/env python
# Refer to http://stackoverflow.com/questions/27590039/running-ansible-playbook-using-python-api

import os
import sys
from lib.ansible_api_playbook import playbook_executor_instance

def check_input(input_pass):
    if input_pass.strip() == '':
        return False
    return input_pass
if __name__ == '__main__':
    bin_path = sys.path[0]
    inventory_host_file = raw_input("Input inventory host path[default: hosts]: ")
    
    if inventory_host_file.strip() == "":
            inventory_host_file = 'hosts'
    if not os.path.exists(inventory_host_file):
        print '[INFO] The hosts inventory does not exist'
        sys.exit()
    os.environ['NC_HOST_FILE'] = inventory_host_file
    
    while True:
        try:
            api_token = raw_input("api_token: ")
            if api_token.strip() == '':
                print 'api_token is not allow empty, [Ctrl+c exit]'
                continue
            else:
                break
        except KeyboardInterrupt:
            print
            sys.exit(1)
    mysql_user = raw_input("mysql dba user[we need use it create monitor user, default is root]: ")
    mysql_password = raw_input("mysql dba user's password: ")
    redis_auth_password = raw_input("redis auth password[if didn't enable redis auth, please input 'enter' key]:")

    if mysql_user.strip() == '':
        mysql_user = 'root'
    mysql_password = check_input(mysql_password)
    redis_auth_password = check_input(redis_auth_password)
    ex_vars = {'api_token': api_token, 'Mysql_user': mysql_user, 'Mysql_password': mysql_password, "Redis_auth_password": redis_auth_password }

    pbex = playbook_executor_instance(ex_vars)
    results = pbex.run()
