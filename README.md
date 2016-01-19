## ansible-tasks
* aliyun_aegis_check: use log callback_plugins

## upgrade ansible
* Install virtualenv
<pre>$ pip install virtualenv</pre>

* Create and active virtual env
<pre>$ virtualenv ansible-new-version
$ . ansible-new-version/bin/active</pre>
* Install the specified version of ansible
<pre>
$ pip install paramiko PyYAML Jinja2 httplib2 six
$ pip install ansible==1.9.4</pre>
