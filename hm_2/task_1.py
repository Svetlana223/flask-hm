'''
Создать страницу, на которой будет форма для ввода имени и электронной почты,
при отпеля,
а также будет произведено перенаправление на страницу приветствия,
где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти»,
при нажатии на которую будет удалён cookie-файл с данными пользователя и
произведено перенаправление на страницу ввода имени и электронной почты.
'''

from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/welcome/', methods=['POST'])
def welcome():
    if request.method == 'POST':
        user_name = request.form['username']
        user_email = request.form['email']
        response = make_response(render_template('welcome.html', username=user_name))
        response.set_cookie('user_data', f'{user_name},{user_email}')
        return response


@app.route('/logout/')
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('user_data')
    return response


if __name__ == '__main__':
    app.run(debug=True)
