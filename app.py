import flask
import flask_wtf
import wtforms
import psycopg2


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
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM books1')
    books = cur.fetchall()
    cur.close()
    conn.close()

    return flask.render_template('index.html', books=books)


@app.route('/book_form/', methods=['GET', 'POST'])
def book_form():
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


if __name__ == '__main__':
    app.run(debug=True)
