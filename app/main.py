from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mebel.db'


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить пароль')
    submit = SubmitField('Войти')


@app.route('/admin')
def admin():
    database = Mebel.query.order_by(Mebel.id).all()
    return render_template('admin.html', title='Вход', database=database)


@app.route('/add', methods=['POST', 'GET'])
def database():
    if request.method == "POST":
        name = request.form['name']
        category = request.form['category']
        count = request.form['count']
        color = request.form['color']
        height = request.form['height']
        weidth = request.form['weidth']
        dep = request.form['dep']
        postav = request.form['postav']
        image = request.form['image']
        dop = request.form['dop']

        article = Mebel(name=name, category=category, count=count, color=color, height=height, weidth=weidth,
                        dep=dep, postav=postav, image=image, dop=dop)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/admin')
        except:
            print('При добавлении произошла ошибка!')
        else:
            return render_template('dobavit.html', title="Добавить запись")



