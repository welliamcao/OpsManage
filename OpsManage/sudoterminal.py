import paramiko
import re
try:
    import simplejson as json
except ImportError:
    import json
from django.utils.encoding import smart_unicode

class ShellHandler(object):

    def __init__(self, ip, username, port, method, credential, timeout = 3, channel_name = None):
        if method not in ['key','password']:
            raise Exception('Authication must be key or password')
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if method == 'password':
            self.ssh.connect(ip, port=port, username=username, password=credential, timeout=timeout)
        else:
            self.ssh.connect(ip, port=port, username=username, key_filename=credential, timeout=timeout)

        channel = self.ssh.invoke_shell()
        self.stdin = channel.makefile('wb')
        self.stdout = channel.makefile('r')
        self.channel_name = channel_name
        

    def __del__(self):
        self.ssh.close()

    @staticmethod
    def _print_exec_out(cmd, out_buf, err_buf, exit_status, channel_name=None ):
        from OpsManage.asgi import channel_layer
        channel_layer.send(channel_name, {'text': json.dumps(['stdout',smart_unicode('command executed: {}'.format(cmd))])})
        print('command executed: {}'.format(cmd))
        print('STDOUT:')
        channel_layer.send(channel_name, {'text': json.dumps(['stdout',smart_unicode('STDOUT:')])})
        for line in out_buf:
            print line, "end="
            channel_layer.send(channel_name, {'text': json.dumps(['stdout',smart_unicode(line.strip('\n'))])})
        channel_layer.send(channel_name, {'text': json.dumps(['stdout',smart_unicode('end of STDOUT')])})
        print('end of STDOUT')
        channel_layer.send(channel_name, {'text': json.dumps(['stdout',smart_unicode('STDERR:')])})
        print('STDERR:')
        for line in err_buf:
            print line, "end="
            channel_layer.send(channel_name, {'text': json.dumps(['stdout',smart_unicode(line, "end=")])})
        channel_layer.send(channel_name, {'text': json.dumps(['stdout',smart_unicode('end of STDERR')])})
        print('end of STDERR')
        channel_layer.send(channel_name, {'text': json.dumps(['stdout',smart_unicode('finished with exit status: {}'.format(exit_status))])})
        print('finished with exit status: {}'.format(exit_status))
        channel_layer.send(channel_name, {'text': json.dumps(['stdout',smart_unicode('------------------------------------')])})
        print('------------------------------------')

    def execute(self, cmd):
        """

        :param cmd: the command to be executed on the remote computer
        :examples:  execute('ls')
                    execute('finger')
                    execute('cd folder_name')
        """
        cmd = cmd.strip('\n')
        self.stdin.write(cmd + '\n')
        finish = 'end of stdOUT buffer. finished with exit status'
        echo_cmd = 'echo {} $?'.format(finish)
        self.stdin.write(echo_cmd + '\n')
        shin = self.stdin
        self.stdin.flush()

        shout = []
        sherr = []
        exit_status = 0
        for line in self.stdout:
            if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
                # up for now filled with shell junk from stdin
                shout = []
            elif str(line).startswith(finish):
                # our finish command ends with the exit status
                exit_status = int(str(line).rsplit()[-1])
                if exit_status:
                    # stderr is combined with stdout.
                    # thus, swap sherr with shout in a case of failure.
                    sherr = shout
                    shout = []
                break
            else:
                # get rid of 'coloring and formatting' special characters
                shout.append(re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]').sub('', line).
                             replace('\b', '').replace('\r', ''))

        # first and last lines of shout/sherr contain a prompt
        if shout and echo_cmd in shout[-1]:
            shout.pop()
        if shout and cmd in shout[0]:
            shout.pop(0)
        if sherr and echo_cmd in sherr[-1]:
            sherr.pop()
        if sherr and cmd in sherr[0]:
            sherr.pop(0)

        self._print_exec_out(cmd=cmd, out_buf=shout, err_buf=sherr, exit_status=exit_status,channel_name=self.channel_name)
        return shin, shout, sherr