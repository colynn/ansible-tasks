##example
$ ansible-playbook check_aliyun_aegis.yml -i ./host -c paramiko -k -vvv  -u username


$ ansible-playbook check_aliyun_aegis.yml -i ./inventory-host.py -c paramiko -s -vvv  -u username
