from src.app import app
from flask import request
from flask import redirect, url_for
from flask import flash
from flask import render_template
from flask import session
from flask import abort
import sqlite3
from .. import config
from flask_argon2 import Argon2  # Required for Argon2 Encryption


# ################# #
#     VARIABLES     #
# ################# #
brand = 'PLMS'
argon2 = Argon2(app)


# ################# #
#     FUNCTIONS     #
# ################# #
def connect_to_db():
    conn = sqlite3.connect(str(config.FILE_DATABASE))
    return conn


def make_userid():
    conn = connect_to_db()
    userid = ''
    with conn:
        cursor = conn.cursor()
        query = "SELECT UserID FROM Users ORDER BY UserID DESC LIMIT 1"
        cursor.execute(query)
        temp_id = cursor.fetchone()
        if temp_id:
            userid_num = int(temp_id[0][1:]) + 1
            userid = 'U{num:{fill}8}'.format(num=userid_num, fill='0')
        else:
            userid = 'U00000001'
    return userid


def convert_permission(user_permission):
    p = user_permission
    return '{:{fill}{width}{type}}'.format(int(p), fill='0', width=5, type='b')


def permission_dictionary(user_permission):
    d = {
            'dev': False,
            'admin': False,
            'manager': False,
            'tenant': False,
            'member': False,
            'binary': None,
            'decimal': user_permission
        }
    b = convert_permission(user_permission)
    if b[0] == '1':
        d['dev'] = True
    else:
        d['dev'] = False
    if b[1] == '1':
        d['admin'] = True
    else:
        d['admin'] = False
    if b[2] == '1':
        d['manager'] = True
    else:
        d['manager'] = False
    if b[3] == '1':
        d['tenant'] = True
    else:
        d['tenant'] = False
    if b[4] == '1':
        d['member'] = True
    else:
        d['member'] = False
    d['binary'] = b
    return d


def get_firm_info():
    conn = connect_to_db()
    with conn:
        cursor = conn.cursor()
        query = "SELECT\
            FirmName,\
            URL,\
            EMail,\
            Telephone,\
            Street_1,\
            Street_2,\
            City,\
            Region,\
            PostalCode\
            FROM FIRM WHERE FirmAlias='sa'"
        cursor.execute(query)
        resp = cursor.fetchone()
    return resp

# ################# #
#    @app.routes    #
# ################# #
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == ['POST']:
        user = request.form
        '''flash("Login requested for user {}, remember me={}".format(
            form.username.data, form.remember_me.data))
        '''
        return render_template('index.html', brand=brand, title='Home', user=result)
    return render_template('index.html', brand=brand, title='Home')


@app.route('/lots')
def lots():
    #get_firm_info()
    return render_template('lots.html', brand=brand, title='Parking Lots')


@app.route('/services')
def services():
    conn = connect_to_db()
    with conn:
        cursor = conn.cursor()
        query = "SELECT * FROM Discounts"
        cursor.execute(query)
        dsc = cursor.fetchall()

        query = "SELECT * FROM Rentals"
        cursor.execute(query)
        rnt = cursor.fetchall()

    return render_template(
        'services.html', brand=brand, title='Services',
        discounts=dsc, rentals=rnt)


@app.route('/status')
def status():
    return render_template('status.html', brand=brand, title='Status')


@app.route('/about')
def about():
    resp = get_firm_info()
    return render_template('about.html', brand=brand, title='About', info=resp)


@app.route('/contact')
def contact():
    return render_template('contact.html', brand=brand, title='Contact')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'userid' in session:
            flash('Log out before logging in again.', 'secondary')
            return redirect(url_for('home'))
        else:
            return render_template('log-in.html', brand=brand, title='Login')
    if request.method == 'POST':
        # ############
        # INITIALIZE
        # ############
        email = request.form.get("email")
        password = request.form.get("password")

        resp = None
        ticket = False

        conn = connect_to_db()

        # ############################
        # RETRIEVE USER INFO FROM DB
        # ############################
        with conn:
            cursor = conn.cursor()
            query = "SELECT * FROM user_info WHERE user_info.EMail=?"
            cursor.execute(query, (email,))
            resp = cursor.fetchone()  # if one value -> fetchone()
            # resp is short for 'response'
            # Columns of resp: UserID, UserName, EMail, Password, PermissionKey

        # #############################
        # USER AND PASSWORD CONTROL
        # #############################
        if resp is None:
            category = 'error'
            flash('No user is found.', category)
            redirect(url_for('login'))
        else:
            # userid = resp[0]
            # usernameDB = resp[1]
            passwordDB = resp[3]
            ticket = argon2.check_password_hash(passwordDB, password)

        # #############################
        # REDIRECT
        # #############################
        if ticket:  # Correct password.
            flash("Logged in as {}". format(resp[1]), 'success')
            session["userid"] = resp[0]
            session["username"] = resp[1]
            session["email"] = resp[2]
            session["permission"] = permission_dictionary(resp[4])
            return redirect(url_for('home'))
        else:  # Wrong password.
            message = "Wrong password"
            category = 'error'
            flash(message, category)
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('userid', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('permission', None)
    flash('Logged Out', 'success')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template(
            'register.html', brand=brand, title='Registration')
    elif request.method == 'POST':
        # ############
        # INITIALIZE
        # ############
        userid = make_userid()
        username = request.form.get("username")
        email = request.form.get("email")
        password = argon2.generate_password_hash(request.form.get("password", '0'))
        permission_key = "1"

        # ############
        # RECORD
        # ############
        conn = connect_to_db()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Users VALUES(?, ?, ?)",
                (userid, username, email))
            cursor.execute(
                "INSERT INTO UsersCreditentials VALUES(?, ?)",
                (userid, password))
            cursor.execute(
                "INSERT INTO UserPermissions VALUES(?, ?)",
                (userid, permission_key))
            conn.commit()

        # ############
        # FINALIZE
        # ############
        flash('User registered.', 'success')
        return redirect(url_for('login'))


@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if request.method == 'GET':
        render_template('manage.html', brand=brand, title='Manage Lots')
    elif request.method == 'POST':
        render_template('manage.html', brand=brand, title='Manage Lots')
        pass
@app.route('/<username>/account', methods=['GET', 'POST'])
def account(username):
    if 'permission' in session:
        print('logged in user is found')
        if request.method == 'GET':
            return render_template('account.html', brand=brand, title='Account')
        elif request.method == 'POST':
            ''' To be changed '''
            return render_template('account.html', brand=brand, title='Account')
    else:
        print('no user. GTFO!')
        abort(403)


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/hi')
def hi():
    return 'Hi'
