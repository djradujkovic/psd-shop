from flask import Blueprint, render_template, request, redirect, url_for
import os

market = Blueprint('market', __name__)

from database import Table

@market.route('/shop')
def shop_show():
    items = Table('shop').load_items()
    return render_template('shop.html', items = items)

@market.route('/dodajproizvod')
def additem_show():
    return render_template('dodajproizvod.html')

@market.route('/dodajproizvod', methods = ['POST'])
def additem_post():
    item = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'ammount': request.form.get('ammount'),
    }
    Table('shop').add_item(item)
    if request.files:
        image = request.files.get('image')
        image.save(os.path.join(os.getcwd() + "/static/proizvodi", item.get('name')+'.png'))
    return redirect(url_for('market.shop_edit'))

@market.route('/obrisiitem/<int:itemid>')
def deleteitem(itemid):
    item = Table('shop').item_by_id(itemid)
    item.remove()
    return redirect(url_for('market.shop_edit'))

@market.route('/edititem/<int:itemid>')
def edititem_show(itemid):
    item = Table('shop').item_by_id(itemid)
    return render_template('edititem.html', item = item)

@market.route('/edititem/<int:itemid>', methods = ['POST'])
def edititem_post(itemid):
    items = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'ammount': request.form.get('ammount'),
    }
    item = Table('shop').item_by_id(itemid)
    item.updates(items)
    if request.files:
        image = request.files.get('image')
        image.save(os.path.join(os.getcwd() + "/static/proizvodi", items.get('name')+'.png'))
    return redirect(url_for('market.shop_edit'))


@market.route('/editshop')
def shop_edit():
    items = Table('shop').load_items()
    return render_template('editshop.html', items = items)