import sqlite3
import os
import datetime


def create_tables(market):
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {market}_products(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    created TEXT NOT NULL, 
    market TEXT NOT NULL, 
    url TEXT NOT NULL, 
    name TEXT NOT NULL, 
    color TEXT NOT NULL, 
    category TEXT, 
    description TEXT, 
    availability TEXT, 
    image TEXT NOT NULL)""")
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {market}_prices(
    price_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    created TEXT NOT NULL, 
    product_id INTEGER NOT NULL, 
    price INT NOT NULL, 
    discount TEXT, 
    FOREIGN KEY (product_id) REFERENCES {market}_products (product_id))""")
    con.commit()


def check_product(amount, **kwargs):
    # if not os.path.exists(db_file):
    create_tables(kwargs['market'])
    if amount == 'one':
        result = cur.execute(f"SELECT * FROM {kwargs['market']}_products").fetchone()
    else:
        result = cur.execute(f"SELECT * FROM {kwargs['market']}_products").fetchall()
    return result


def insert_data_to_products(**kwargs):
    query = f'INSERT INTO {kwargs["market"]}_products (created, market, url, name, color, category, description, availability, image) ' \
            f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cur.execute(query, (datetime.datetime.now().strftime('%Y/%m/%d - %H:%M:%S'),
                        kwargs['market'],
                        kwargs['url'],
                        kwargs['name'],
                        kwargs['color'],
                        kwargs['category'],
                        kwargs['description'],
                        kwargs['availability'],
                        kwargs['image']))
    con.commit()


def insert_data_to_db_prices(**kwargs):
    cur.execute(f'INSERT INTO {kwargs["market"]}_prices (created, product_id, price, discount) VALUES (?, ?, ?, ?)',
                (datetime.datetime.now().strftime('%Y/%m/%d - %H:%M:%S'),
                 kwargs['product_id'],
                 kwargs['price'],
                 kwargs['discount']))
    con.commit()


# def last_row(market):
#     result = cur.execute('SELECT * FROM products '
#                          'WHERE market="%s" '
#                          'ORDER BY product_id '
#                          'DESC LIMIT 1' % market).fetchone()
#     return result
def last_row(**kwargs):
    result = cur.execute(f'SELECT * FROM {kwargs["market"]}_products '
                         'ORDER BY product_id '
                         'DESC LIMIT 1').fetchone()
    return result


def last_n_prices_rows(**kwargs):
    last_n_prices = cur.execute(f'SELECT * FROM {kwargs["market"]}_prices '
                f'WHERE product_id={kwargs["product_id"]} '
                f'ORDER BY created '
                f'DESC LIMIT {kwargs["last_rows"]}').fetchall()
    last_n_prices_text = ''
    for data_price in last_n_prices:
        if data_price[4] != '':
            dscnt = f' ({data_price[4]}%)'
        else:
            dscnt = ''
        last_n_prices_text += f'{data_price[1].split(" - ")[0]} - {data_price[3]} ₸{dscnt}\n'
    return last_n_prices_text


def find_product_price(finded_product, **kwargs):
    return cur.execute(f'SELECT * FROM {kwargs["market"]}_prices '
                       f'WHERE product_id={finded_product} '
                       f'ORDER BY created '
                       f'DESC LIMIT 1').fetchone()


db_file = 'odezhda.db'
con = sqlite3.connect(db_file)
con.execute('PRAGMA foreign_keys = 1')
cur = con.cursor()
# create_tables()
