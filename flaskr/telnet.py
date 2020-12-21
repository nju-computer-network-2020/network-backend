from telnetlib import Telnet
import time
import topology as tp


def config_router(hostname, router_info):
    target = TelnetConnection(hostname, router_info['ip'], router_info['password'])
    return target.execute_commands(tp.commands[hostname])


def _input_to_telnet(command: str):
    return command.encode('ascii') + b'\r\n'


class TelnetConnection:
    def __init__(self, hostname, ip, password):
        self.hostname = hostname
        self.ip = ip
        self.password = password

    def _connect(self, func=lambda x: None):
        try:
            with Telnet(self.ip) as tn:
                tn.read_until(b'Password:', timeout=2)
                tn.write(_input_to_telnet(self.password))
                time.sleep(2)

                # if password is wrong, telnet will request the user retype it
                result = tn.read_until(b'Password:',timeout=2)
                if b'Password:' in result:
                    return 'invalidPasswd'
                elif b'>' in result:
                    func(tn)
                    return 'success'
        except (TimeoutError, ConnectionRefusedError):
            return 'ipErr'

    def test_connection(self):
        return self._connect()

    @property
    def profiles(self):
        return {
            'hostname': self.hostname,
            'ip': self.ip,
            'password': self.password
        }

    def execute_commands(self, commands):
        def execute(tn):
            # enter enable mode
            tn.write(_input_to_telnet('enable'))
            tn.read_until(b'Password', timeout=2)
            tn.write(_input_to_telnet('123456'))

            for command in commands:
                tn.write(_input_to_telnet(command))
                time.sleep(1)
                print(tn.read_eager())

        return self._connect(execute)
