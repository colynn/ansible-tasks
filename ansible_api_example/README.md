
### Prepare Inventory
    1> cat > hosts << _
    web1 ansible_host=1.1.1.1 ansible_port=22 ansible_user=ncadmin3
    web2 ansible_host=1.1.1.1 ansible_port=22 ansible_user=ncadmin1
    db1 ansible_host=1.1.1.1 ansible_port=22  ansible_user=ncadmin2
    _
    or 
    using 0_prepare_host_list.py generate inventory host list.

### run example_run.py(Interactive input needed information)

    python example_run.py

    
    
