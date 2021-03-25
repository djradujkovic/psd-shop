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

@market.route('/korpaadd/<int:itemid>/<int:ammount>')
def korpa_add(itemid, ammount):
    user = Table('users').item_by_id(session['ID'])
    korpe = Table('korpe')
    korpa = korpe.first({'shopid': user.shopid, 'itemid': itemid, 'userid': user.ID})
    if korpa:
        korpa.update({'ammount': korpa.ammount+ammount})
    else:
        korpe.add_item({'shopid': user.shopid, 'userid': user.ID, 'itemid': itemid, 'ammount': ammount})
    return redirect(url_for('market.shop_show'))

@market.route('/kupi')
def korpa_buy():
    user = Table('users').item_by_id(session['ID'])
    korpe = Table('korpe').find_items({'shopid': user.shopid, 'userid': user.ID})
    shop = Table('shop')
    user.update({'shopid': user.shopid+1})
    narudzbe = Table('narudzbe')
    lastid = narudzbe.add_item({'kupac': user.name, 'cijena': sum(shop.item_by_id(i.itemid).price*i.ammount for i in korpe)})
    for korpa in korpe:
        Table('narudzba').add_item({'shopid': lastid, 'userid': user.ID, 'itemid': korpa.itemid, 'ammount': korpa.ammount})
        korpa.remove()
    return redirect(url_for('market.shop_show'))

@market.route('/narudzbe')
def narudzbe_show():
    narudzbe = Table('narudzbe').load_items()
    narudzba = Table('narudzba').load_items()
    shop = Table('shop')
    return render_template('narudzbe.html', na = narudzbe, n = narudzba, shop = shop)


@market.route('/posaljinarudzbu/<int:shopid>')
def narudzbe_send(shopid):
    narudzba = Table('narudzbe').item_by_id(shopid)
    items = Table('narudzba').find_items({'shopid': shopid})
    stare_narudzbe = Table('stare_narudzbe')
    stara_narudzba = Table('stara_narudzba')
    for narudzbe in items:
        stara_narudzba.add_item(narudzbe.itemdict)
        narudzbe.remove()
    stare_narudzbe.add_item(narudzba.itemdict)
    narudzba.remove()
    return redirect(url_for('market.narudzbe_show'))

    
