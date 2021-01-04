import time
from telnetlib import Telnet
from typing import Callable, Any

import topology as tp


def config_router(hostname, router_info):
    target = RouterTelnetConnection(hostname, router_info['ip'], router_info['password'])
    return target.execute_commands(tp.commands[hostname])


def run_test(hostname, router_info, expected_string):
    target = RouterTelnetConnection(hostname, router_info['ip'], router_info['password'])
    exec_result = target.execute_tests(tp.test_commands[hostname])

    if exec_result == 'invalidPasswd' or exec_result == 'ipErr':
        return False, exec_result

    print(exec_result)
    return exec_result


def run_pc_test(hostname, pc_info):
    target = PCTelnetConnection(hostname, pc_info['ip'], pc_info['password'])
    exec_result = target.execute_tests(tp.test_commands[hostname])
    print(exec_result)

    if exec_result == 'invalidPasswd' or exec_result == 'ipErr':
        return False, exec_result

    return exec_result


def _input_to_telnet(command: str):
    return command.encode('ascii') + b'\r\n'


class PCTelnetConnection:
    def __init__(self, hostname, ip, password):
        self.hostname = hostname
        self.ip = ip
        self.password = password

    def _connect(self, func: Callable[[Any], Any] = lambda x: 'success'):
        try:
            with Telnet(self.ip) as tn:
                # try to login
                tn.read_until(b'login:', timeout=5)
                tn.write(_input_to_telnet(self.hostname))
                tn.read_until(b'password', timeout=5)
                tn.write(_input_to_telnet(self.password))
                time.sleep(0.1)

                # if password is wrong, telnet will request the user retype it
                result = tn.read_until(b'login:', timeout=1)
                print(result)
                if b'login:' in result:
                    return 'invalidPasswd'
                elif b'>' in result:
                    # execute user defined function
                    return func(tn)
                else:
                    return result
        except (TimeoutError, ConnectionRefusedError):
            return 'ipErr'

    def execute_tests(self, test_commands):
        def execute(tn):
            telnet_output = []
            test_result = True
            for command, expected in test_commands:
                tn.write(_input_to_telnet(command))
                if expected is not None:
                    # read messages from telnet and test them with expected string
                    time.sleep(0.1)
                    response = tn.read_until(expected, timeout=5)
                    response += tn.read_eager()
                    if expected not in response:
                        test_result = False
                    telnet_output.append(response.decode('gbk'))

            return test_result, telnet_output

        return self._connect(execute)


class RouterTelnetConnection:
    def __init__(self, hostname, ip, password):
        self.hostname = hostname
        self.ip = ip
        self.password = password

    def _connect(self, func: Callable[[Any], Any] = lambda x: 'success', enabled=False):
        try:
            with Telnet(self.ip) as tn:
                tn.read_until(b'Password:', timeout=2)
                tn.write(_input_to_telnet(self.password))
                time.sleep(0.5)

                # if password is wrong, telnet will request the user retype it
                result = tn.read_until(b'Password:', timeout=2)
                if b'Password:' in result:
                    return 'invalidPasswd'
                elif b'>' in result:
                    if enabled:
                        # enter enable mode
                        tn.write(_input_to_telnet('enable'))
                        tn.read_until(b'Password', timeout=2)
                        tn.write(_input_to_telnet('123456'))

                    # execute user defined function
                    return func(tn)
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
            for command in commands:
                tn.write(_input_to_telnet(command))
                time.sleep(0.1)
                response = tn.read_eager()
                print(response)

            return 'success'

        return self._connect(execute, enabled=True)

    def execute_tests(self, test_commands):
        def execute(tn):
            telnet_output = []
            test_result = True
            for command, expected in test_commands:
                tn.write(_input_to_telnet(command))
                if expected is not None:
                    # read messages from telnet and test them with expected string
                    response = tn.read_until(expected, timeout=5)
                    response += tn.read_eager()
                    if expected not in response:
                        test_result = False
                    telnet_output.append(response.decode('ascii'))

            return test_result, telnet_output

        return self._connect(execute, enabled=True)
