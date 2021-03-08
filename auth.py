from flask import Blueprint, render_template, request, session, redirect, url_for

auth = Blueprint('auth', __name__)



@auth.route('/login')
def login_show():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    from database import Table
    user = {
        'name': request.form.get('name'),
        'password': request.form.get('password')
    }
    users = Table('users')
    userdb = users.first({'name': user.get('name')})
    if userdb:
        if user.get('password') == userdb.password:
            session['ID'] = userdb.ID
            return redirect(url_for('main.index'))
    return redirect(url_for('auth.login_show'))

@auth.route('/signup')
def signup_show():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    from database import Table
    user = {
        'name': request.form.get('name'),
        'password': request.form.get('password')
    }
    users = Table('users')
    users.add_item(user)
    session['ID'] = users.first({'name': user.get('name')})
    return redirect(url_for('main.index'))