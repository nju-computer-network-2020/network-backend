import topology as tp


def config_router(hostname, router_info):
    return 'success'


def run_test(hostname, router_info):
    return 'success', ['Nothing to show']


# noinspection PyMethodMayBeStatic
class RouterTelnetConnection:
    def __init__(self, hostname, ip, password):
        self.hostname = hostname
        self.ip = ip
        self.password = password

    def test_connection(self):
        return 'success', None

    @property
    def profiles(self):
        return {
            'hostname': self.hostname,
            'ip': self.ip,
            'password': self.password
        }

    def execute_commands(self, commands):
        return 'success', ['Nothing to show']


class PCTelnetConnection:
    def __init__(self, hostname, ip, password):
        self.hostname = hostname
        self.ip = ip
        self.password = password

