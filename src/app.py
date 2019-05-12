from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)


# ################# #
#     VARIABLES     #
# ################# #
brand = 'PLMS'


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
    return render_template('index.html', brand=brand, title='Home')


@app.route('/services')
def services():
    return render_template('services.html', brand=brand, title='Services')


@app.route('/about')
def about():
    return render_template('about.html', brand=brand, title='About')


@app.route('/contact')
def contact():
    return render_template('contact.html', brand=brand, title='Contact')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('log-in.html', brand=brand, title='Login')


@app.route('/hi')
def hi():
    return 'Hi'


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
