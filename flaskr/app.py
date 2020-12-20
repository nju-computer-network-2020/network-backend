from flask import Flask, request

app = Flask(__name__)


@app.route('/connect')
def connect_telnet():
    hostname = request.args.get('hostname')
    ip_add = request.args.get('ipAdd')
    password = request.args.get('password')


@app.route('/autoConfig')
def do_configuration():
    pass


@app.route('/testResult')
def do_test():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0')
