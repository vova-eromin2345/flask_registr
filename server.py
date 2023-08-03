from flask import Flask, render_template, request, redirect, url_for, flash, abort
import sqlite3
from sql_tools import * 


app = Flask(__name__)

app.config['SECRET_KEY'] = 'pa66word'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in(): # Войти
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']

        create_table('users.db', 'users', 'login', 'password')
        all = read_from_db('users.db', 'users', '*')
        if (login,password) in all:
            print(login, password)
            return render_template('user_page.html', login=login, password=password)
        else:
            flash(u"Не верный логин или пароль", 'error')

    return render_template('sign-in.html', action="sign_in")


@app.route('/sign-up', methods=["GET", "POST"])
def sign_up(): # Реестрация
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']

        create_table("users.db", 'users', 'login', 'password')
        all_logins = read_from_db('users.db', 'users', 'login')
        
        
        if (login,) in all_logins:
            flash(u"Логин уже занят!", 'error')
        else:
            write_to_db('users.db', 'users', ('login', 'password'), (login, password))

            return render_template('user_page.html', login=login, password=password)
    
    return render_template('sign-up.html', action='sign_up')


if __name__ == "__main__":
    app.run('127.0.0.1', 5000)