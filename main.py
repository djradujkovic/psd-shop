from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def index():
    from database import Table
    items = Table('shop').load_items()
    # users = Table('users').create_table(columns='ID int AUTO_INCREMENT, name VARCHAR(24) UNIQUE, password VARCHAR(24)', primary='ID')
    return render_template('index.html', items = items)

@main.route('/onama')
def onama():
    return render_template('about.html')

@main.route('/blog')
def blog():
    return render_template('blog.html')

@main.route('/kontakt')
def kontakt():
    return render_template('contact.html')