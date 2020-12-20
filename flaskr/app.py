from flask import Flask, request, session
from telnet import TelnetConnection, config_router
from collections import namedtuple
import topology as tp

app = Flask(__name__)

ResultMessage = namedtuple('result', ['success', 'errMessage'])


@app.route('/connect', methods=['GET'])
def connect_telnet():
    hostname = request.args.get('hostname')
    ip_add = request.args.get('ipAdd')
    password = request.args.get('password')

    # validate parameters
    if hostname is None or ip_add is None or password is None:
        return ResultMessage(False, 'incompleteParams')
    if hostname not in tp.valid_hosts:
        return ResultMessage(False, 'invalidHostname')

    # test connection
    telnet = TelnetConnection(hostname, ip_add, password)
    connect_result = telnet.test_connection()
    if connect_result == 'success':
        session[hostname] = telnet.profiles
        return ResultMessage(True, '')._asdict()
    else:
        return ResultMessage(False, connect_result)._asdict()


@app.route('/autoConfig')
def do_configuration():
    # get saved information from session
    # use these information to do configuration
    if not tp.valid_hosts.issubset(session.keys()):
        return ResultMessage(False, 'hostIncomplete')._asdict()

    # config each router by telnet
    for host in tp.valid_hosts:
        config_router(host, session[host])

    return ResultMessage(True, '')._asdict()


@app.route('/testResult')
def do_test():
    # return NAT table of RTB
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0')
