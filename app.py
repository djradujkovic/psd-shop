from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'djole'
app.config['MYSQL_PASSWORD'] = 'nespa17er'
app.config['MYSQL_DB'] = 'test'

app.config['MY_SECRET'] = 'blabla'

mysql = MySQL(app)

from main import main
app.register_blueprint(main)

from shop import market
app.register_blueprint(market)


if __name__ == '__main__':
    app.run(debug=True)