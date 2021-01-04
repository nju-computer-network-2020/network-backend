from collections import namedtuple

from flask import Flask, request, session, make_response
from flask_cors import CORS

import topology as tp
from telnet import RouterTelnetConnection, config_router, run_test, run_pc_test

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app, supports_credentials=True)

ResultMessage = namedtuple('ResultMessage', ['success', 'errMessage'])
TestResult = namedtuple('TestResult', ['success', 'message'])


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
    telnet = RouterTelnetConnection(hostname, ip_add, password)
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
    # if not tp.valid_hosts.issubset(session.keys()):
    #     return ResultMessage(False, 'hostIncomplete')._asdict()

    # config each router by telnet
    for router_profile in tp.router_profiles:
        result = config_router(router_profile['hostname'], router_profile)
        if result != 'success':
            return ResultMessage(False, result)._asdict()

    return ResultMessage(True, '')._asdict()


@app.route('/testResult')
def do_test():
    # return NAT table of RTB
    result = run_pc_test(tp.PC2, tp.pc2_profile)
    return TestResult(*result)._asdict()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
