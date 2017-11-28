# Refer to http://stackoverflow.com/questions/27590039/running-ansible-playbook-using-python-api
import os
import sys
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

# Callback
from ansible import constants as C
from default import DefaultCallback


def playbook_executor_instance(ex_vars):
    """
    Args:
        re_user: string, remote_user
        ex_vars: dict
    """
    variable_manager = VariableManager()
    loader = DataLoader()
    bin_path = sys.path[0]
    inventory = Inventory(loader=loader, variable_manager=variable_manager,  host_list=bin_path + '/lib/inventory-host.py')
    playbook_path = bin_path + '/site.yml'

    if not os.path.exists(playbook_path):
        print '[INFO] The playbook does not exist'
        sys.exit()

    Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax',
                                     'connection', 'module_path', 'forks', 'remote_user', 'private_key_file',
                                     'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args',
                                     'become', 'become_method', 'become_user', 'verbosity', 'check']
                         )

    options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='paramiko',
                      module_path=None, forks=100, remote_user=None, private_key_file=None,
                      ssh_common_args='', ssh_extra_args='', sftp_extra_args=None, scp_extra_args=None,
                      become=True, become_method='sudo', become_user='root', verbosity=None, check=False
                      )
    variable_manager.extra_vars = ex_vars

    passwords = {}

    results_callback = DefaultCallback()
    C.DEFAULT_STDOUT_CALLBACK = results_callback
    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,
                        loader=loader, options=options, passwords=passwords)
    return pbex
