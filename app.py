import flask
import flask_wtf
import wtforms
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash


class LogForm(flask_wtf.FlaskForm):
    login = wtforms.StringField('Login')
    password = wtforms.PasswordField('Password')
    submit = wtforms.SubmitField('Sign in')


class RegForm(flask_wtf.FlaskForm):
    login = wtforms.StringField('Login')
    password = wtforms.PasswordField('Password')
    email = wtforms.StringField('Email')
    submit = wtforms.SubmitField('Sign up!')


class AddForm(flask_wtf.FlaskForm):
    title = wtforms.StringField('Title')
    author = wtforms.StringField('Author')
    review = wtforms.TextAreaField('Review')
    pages_num = wtforms.IntegerField("Pages")
    submit = wtforms.SubmitField('Submit!')


def get_db_connection():
    conn = psycopg2.connect(user='postgres',
                            database='flask_db',
                            host='localhost',
                            password='0000')

    return conn


app = flask.Flask(__name__)

app.config['SECRET_KEY'] = 'Aa'


@app.route('/')
def index():
    if 'userLogged' not in flask.session:
        return flask.redirect(flask.url_for('log_in'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM books1')
    books = cur.fetchall()
    cur.close()
    conn.close()

    return flask.render_template('index.html', books=books)


@app.route('/book_form/', methods=['GET', 'POST'])
def book_form():
    if 'userLogged' not in flask.session:
        return flask.redirect(flask.url_for('log_in'))

    form = AddForm()

    if flask.request.method == 'GET':
        return flask.render_template('BookForm.html', form=form)
    else:
        conn = get_db_connection()
        cur = conn.cursor()

        f_title = form.title.data
        f_author = form.author.data
        f_review = form.review.data
        f_pages_num = form.pages_num.data

        cur.execute('INSERT INTO books1 (title, author, review, pages_num)'
                    'VALUES (%s, %s, %s, %s)',
                    (f_title,
                     f_author,
                     f_review,
                     f_pages_num)
                    )
        conn.commit()
        cur.close()
        conn.close()

        return flask.render_template('BookForm.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'userLogged' in flask.session:
        return flask.redirect(flask.url_for('index'))

    reg_form = RegForm()
    conn = get_db_connection()
    cur = conn.cursor()
    if flask.request.method == 'GET':
        return flask.render_template("registration.html", form=reg_form)
    else:
        cur.execute("SELECT * FROM users")
        users_data = cur.fetchall()

        f_login = reg_form.login.data
        f_psw = reg_form.password.data
        f_email = reg_form.email.data

        for user in users_data:
            if user[1] == f_login:
                flask.flash("Пользователь с таким логином уже зарегистрирован!", category="error")
                return flask.render_template("registration.html", form=reg_form)

        psw_hash = generate_password_hash(f_psw)
        cur.execute('INSERT INTO users (login, password, email)'
                    'VALUES (%s, %s, %s)',
                    (f_login, psw_hash, f_email))
        conn.commit()
        cur.close()
        conn.close()

        return flask.redirect(flask.url_for('log_in'))


@app.route('/login/', methods=['GET', 'POST'])
def log_in():
    if 'userLogged' in flask.session:
        return flask.redirect(flask.url_for('index'))

    log_form = LogForm()
    conn = get_db_connection()
    cur = conn.cursor()
    if flask.request.method == "GET":
        return flask.render_template("login.html", form=log_form)
    else:
        f_login = log_form.login.data
        f_psw = log_form.password.data

        cur.execute('SELECT * FROM users')
        users_data = cur.fetchall()

        for user in users_data:
            if f_login == user[1] and check_password_hash(user[2], f_psw):
                flask.session["userLogged"] = f_login
                cur.close()
                conn.close()
                return flask.redirect(flask.url_for('index'))

        flask.flash("Ведённые данные неверны!", category="error")

        return flask.render_template("login.html", form=log_form)


if __name__ == '__main__':
    app.run(debug=True)
