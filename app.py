from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'djole'
app.config['MYSQL_PASSWORD'] = 'nespa17er'
app.config['MYSQL_DB'] = 'test'

app.config['MY_SECRET'] = 'blabla'

mysql = MySQL(app)

@app.route('/')
def index():
    from database import Table
    shop = Table('shop')
    shop.add_item({'ID': 1, 'name': 'Majica', 'price': 152, 'ammount': 100})
    shop.add_item({'ID': 2, 'name': 'Majica', 'price': 152, 'ammount': 100})
    # shop.item_by_id(2).remove()
    # shop.create_table()
    return str(shop.find_items(where={'name': 'Majica'}))

if __name__ == '__main__':
    app.run(debug=True)