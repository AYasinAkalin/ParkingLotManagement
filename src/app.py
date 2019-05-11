from flask import Flask
from flask import request
from flask import render_template
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
def home():
    return render_template('index.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login')
def login():
    return render_template('log-in.html')


@app.route('/hi')
def hi():
    return 'Hi'


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
