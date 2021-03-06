# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# NOTE: in Ansible 1.2 or later general logging is available without
# this plugin, just set ANSIBLE_LOG_PATH as an environment variable
# or log_path in the DEFAULTS section of your ansible configuration
# file.  This callback is an example of per hosts logging for those
# that want it.

TIME_FORMAT="%b %d %Y %H:%M:%S"
MSG_FORMAT="%(host)s \t %(data)s\n"

def log(host, category, data):

    path = "./aliyun_list.txt"

    if type(data) == dict:
        if 'verbose_override' in data:
            # avoid logging extraneous data from facts
            stdout = 'omitted'
        else:
            data = data.copy()
        if ('stdout' in data.keys()):
	    stdout=data['stdout']
    fd = open(path, "a")
    if ( stdout == 'no clean'):
	fd.write(MSG_FORMAT % dict(host=host, data=stdout))
    else:
        for line in stdout.split('\n'):
	   if line == '':
	     continue
	   line=line.split('"')[1].split()[1]
	   #print line.split('"')
	   fd.write(MSG_FORMAT % dict(host=host, data=line))
    fd.write('\n')
    fd.close()


class CallbackModule(object):
    """
    logs playbook results
    """

    def on_any(self, *args, **kwargs):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        log(host, 'FAILED', res)

    def runner_on_ok(self, host, res):
        log(host, 'OK', res)

    def runner_on_skipped(self, host, item=None):
        log(host, 'SKIPPED', '...')

    def runner_on_unreachable(self, host, res):
        log(host, 'UNREACHABLE', res)

    def runner_on_no_hosts(self):
        pass

    def runner_on_async_poll(self, host, res, jid, clock):
        pass

    def runner_on_async_ok(self, host, res, jid):
        pass

    def runner_on_async_failed(self, host, res, jid):
        log(host, 'ASYNC_FAILED', res)

    def playbook_on_start(self):
        pass

    def playbook_on_notify(self, host, handler):
        pass

    def playbook_on_no_hosts_matched(self):
        pass

    def playbook_on_no_hosts_remaining(self):
        pass

    def playbook_on_task_start(self, name, is_conditional):
        pass

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
        pass

    def playbook_on_setup(self):
        pass

    def playbook_on_import_for_host(self, host, imported_file):
        log(host, 'IMPORTED', imported_file)

    def playbook_on_not_import_for_host(self, host, missing_file):
        log(host, 'NOTIMPORTED', missing_file)

    def playbook_on_play_start(self, name):
        pass

    def playbook_on_stats(self, stats):
        pass
