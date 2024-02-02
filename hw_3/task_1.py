'''
Создать форму для регистрации пользователей на сайте.
Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.
'''

from flask import Flask, redirect, url_for, render_template
from flask_wtf.csrf import CSRFProtect
from hw_3.form_1 import RegistrationForm
from hw_3.models_1 import db, User
from hashlib import sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
app.config['SECRET_KEY'] = b'aa07dcc1c9c38e29df1bc19e14a764c18f9ce000a1a6fc9e385aabe6bbd02f1d'
csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=sha256(form.password.data.encode(encoding='utf-8')).hexdigest(),
                    confirm_password= sha256(form.password.data.encode(encoding='utf-8')).hexdigest())

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.cli.command('init-db')
def create():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
