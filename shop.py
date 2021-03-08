from flask import Blueprint, render_template

market = Blueprint('market', __name__)

from database import Table

@market.route('/shop')
def shop_show():
    items = Table('shop').load_items()
    return render_template('shop.html', items = items)

@market.route('/editshop')
def editshop():
    Table('shop').add_item({'ID': 1, 'name': 'Majica', 'price': 152, 'ammount': 100})
    Table('shop').add_item({'ID': 2, 'name': 'Majica', 'price': 152, 'ammount': 100})
    items = Table('shop').load_items()
    print(items)
    return render_template('editshop.html', items = items)