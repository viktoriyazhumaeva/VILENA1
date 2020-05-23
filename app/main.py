from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mebel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg'])
db = SQLAlchemy(app)

class Mebel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=True)
    category = db.Column(db.Text(20), nullable=True)
    count = db.Column(db.Integer, nullable=True)
    color = db.Column(db.String(50), nullable=True)
    height = db.Column(db.Integer, nullable=True)
    weidth = db.Column(db.Integer, nullable=True)
    dep = db.Column(db.Integer, nullable=True)
    postav = db.Column(db.String(50), nullable=True)
    image = db.Column(db.Text)
    dop = db.Column(db.Text)

    def __repr__(self):
        return '<Mebel %r>' %self.id



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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    check_password = 'admin123'
    check_username = 'vilena'
    if form.validate_on_submit() and request.method == 'POST':
        if form.password.data == check_password and form.username.data == check_username:
            return redirect('/admin')
        else:
            return 'Error'
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/admin/<int:id>/delete')
def delete(id):
    article = Mebel.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/admin')
    except:
        return "При удалении произошла ошибка!"


    if __name__ == '__main__':
        app.run(debug=True)




