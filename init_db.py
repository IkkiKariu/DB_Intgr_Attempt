import psycopg2

conn = psycopg2.connect(database='flask_db',
                        host='localhost',
                        password='0000',
                        user='postgres')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS books1;')

cur.execute('CREATE TABLE books1('
            'id serial primary key,'
            'title varchar(255) NOT NULL,'
            'author varchar(100) NOT NULL,'
            'review text NOT NULL,'
            'pages_num integer NOT NULL,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);')

cur.execute('INSERT INTO books1 (title, review, author, pages_num )'
            'VALUES(%s, %s, %s, %s)',
            ('Tale of two cities',
             'Great classic',
             'Charles Dickens',
             432)
            )

conn.commit()
cur.close()
conn.close()
