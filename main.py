import sqlite3
import datetime

db = sqlite3.connect("online_store.db")

# db.execute('''CREATE TABLE IF NOT EXISTS products (
#             product_id INTEGER PRIMARY KEY,
#             name TEXT NOT NULL,
#             category TEXT NOT NULL,
#             price REAL NOT NULL);
# ''')

# db.execute('''CREATE TABLE IF NOT EXISTS customers ( 
#           customer_id INTEGER PRIMARY KEY, 
#           first_name TEXT NOT NULL, 
#           last_name TEXT NOT NULL, 
#           email TEXT NOT NULL UNIQUE );''')

# db.execute('''CREATE TABLE IF NOT EXISTS orders ( 
#           order_id INTEGER PRIMARY KEY, 
#           customer_id INTEGER NOT NULL, 
#           product_id INTEGER NOT NULL, 
#           quantity INTEGER NOT NULL, 
#           order_date DATE NOT NULL, 
#           FOREIGN KEY (customer_id) REFERENCES customers(customer_id), 
#           FOREIGN KEY (product_id) REFERENCES products(product_id) );''')

def add_product():
    name = input("Name: ")
    category = input("Category: ")
    price = float(input("Price: "))
    db.execute('''INSERT INTO products(name, category, price) 
               VALUES (?, ?, ?);''', (name, category, price))
    db.commit()

def add_user():
    f_name = input("First name: ")
    l_name = input("Last name: ")
    email = input("Email: ")
    db.execute('''INSERT INTO customers(first_name, last_name, email) 
               VALUES (?, ?, ?);''', (f_name, l_name, email))
    db.commit()

def add_order():
    customer_id = int(input("Customer ID: "))
    product_id = int(input("Product ID: "))
    quantity = int(input("Quantity: "))
    order_date = datetime.datetime.now().replace(microsecond=0)
    db.execute('''INSERT INTO orders(customer_id, product_id, quantity, order_date)
               VALUES (?, ?, ?, ?);''', (customer_id, product_id, quantity, order_date))
    db.commit()

def income():
    a = db.execute('''SELECT SUM(o.quantity * p.price) 
               FROM orders o 
               INNER JOIN products p ON p.product_id == o.product_id;''')
    print(a.fetchone())

def orders_by_customer():
    info = db.execute('''SELECT c.first_name, COUNT(o.order_id) 
                      FROM orders o 
                      INNER JOIN customers c ON o.customer_id == c.customer_id
                      GROUP BY c.first_name;''')
    print(info.fetchall())

def avg_order_price():
    info = db.execute('''SELECT AVG(o.quantity * p.price)
                      FROM orders o
                      INNER JOIN products p ON o.product_id == p.product_id;''')
    print(info.fetchone())

def update_price():
    category = input("Category: ")
    db.execute('''UPDATE products
               SET price = price * 1.1
               WHERE category == (?)''', (category,))
    db.commit()

while True:
    print('''
Що ви хочете зробити?
1 - Додавання продуктів:
2 - Додавання клієнтів:
3 - Замовлення товарів:
4 - Сумарний обсяг продажів:
5 - Кількість замовлень на кожного клієнта:
6 - Середній чек замовлення:
7 - Найбільш популярна категорія товарів:
8 - Загальна кількість товарів кожної категорії:
9 - Оновлення цін категорії на 10% більші:
10 - Показати усіх користувачів
11 - Показати усі продукти
12 - Показати усі замовлення(Joined)
0 - Вийти:''')
    cmd = int(input("Choose an option: "))

    match cmd:
        case 0:
            break
        case 1:
            add_product()
        case 2:
            add_user()
        case 3:
            add_order()
        case 4:
            income()
        case 5:
            orders_by_customer()
        case 6:
            avg_order_price()
        case 9: 
            update_price()