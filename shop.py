from flask import Blueprint, render_template, request, redirect, url_for, session
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

@market.route('/proizvod/<int:itemid>')
def item_show(itemid):
    item = Table('shop').item_by_id(itemid)
    return render_template('proizvod.html', item = item)

@market.route('/editshop')
def shop_edit():
    items = Table('shop').load_items()
    return render_template('editshop.html', items = items)

@market.route('/korpa')
def korpa_show():
    user = Table('users').item_by_id(session['ID'])
    items = Table('korpe').find_items({'userid': user.ID, 'shopid': user.shopid})
    shop = Table('shop')
    total = sum(shop.item_by_id(i.itemid).price*i.ammount for i in items)
    return render_template('cart.html', items = items, shop = shop, total = total)

@market.route('/korpaadd/<int:itemid>')
def korpa_add(itemid):
    user = Table('users').item_by_id(session['ID'])
    korpe = Table('korpe')
    korpe.add_item({'shopid': user.shopid, 'userid': user.ID, 'itemid': itemid, 'ammount': 1})
    return redirect(url_for('market.shop_show'))
