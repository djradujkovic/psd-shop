from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'djole'
app.config['MYSQL_PASSWORD'] = 'nespa17er'
app.config['MYSQL_DB'] = 'test'

app.config['SECRET_KEY'] = 'blabla'

mysql = MySQL(app)

from main import main
app.register_blueprint(main)

from shop import market
app.register_blueprint(market)

from auth import auth
app.register_blueprint(auth)


if __name__ == '__main__':
    app.run(debug=True)