from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/onama')
def onama():
    return render_template('about.html')

@main.route('/blog')
def blog():
    return render_template('blog.html')

@main.route('/kontakt')
def kontakt():
    return render_template('contact.html')