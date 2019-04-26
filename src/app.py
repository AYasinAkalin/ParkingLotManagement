from flask import Flask
from flask import request
app = Flask(__name__)


# ################# #
#     FUNCTIONS     #
# ################# #
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# ################# #
#    @app.routes    #
# ################# #
@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/hi')
def hi():
    return 'Hi'


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
