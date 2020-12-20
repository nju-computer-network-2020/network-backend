from telnetlib import Telnet
import time
import topology as tp


def config_router(hostname, router_info):
    target = TelnetConnection(hostname, router_info['ip'], router_info['password'])
    target.execute_commands(tp.commands[hostname])


def _input_to_telnet(command: str):
    return command.encode('ascii') + b'\n'


class TelnetConnection:
    def __init__(self, hostname, ip, password):
        self.hostname = hostname
        self.ip = ip
        self.password = password

    def test_connection(self):
        try:
            with Telnet(self.ip) as tn:
                tn.read_until(b'Password:')
                tn.write(_input_to_telnet(self.password))
                time.sleep(2)

                # if password is wrong, telnet will request the user retype it
                result = tn.read_until(b'Password:')
                if b'Password:' in result:
                    return 'invalidPasswd'
                elif b'>' in result:
                    return 'success'
        except TimeoutError:
            return 'ipErr'
        except ConnectionRefusedError:
            return 'refused'

    @property
    def profiles(self):
        return {
            'hostname': self.hostname,
            'ip': self.ip,
            'password': self.password
        }

    def execute_commands(self, commands):
        with Telnet(self.ip) as tn:
            tn.read_until(b'Password:')
            tn.write(_input_to_telnet(self.password))
            time.sleep(2)

            # enter enable mode
            tn.write(_input_to_telnet('enable'))
            tn.read_until(b'Password')
            tn.write('123456')

            for command in commands:
                tn.write(_input_to_telnet(command))
