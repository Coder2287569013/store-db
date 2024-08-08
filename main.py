#importing libs
import sqlite3
import datetime

#connecting DB
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
#           FOREIGN KEY (product_id) REFERENCES products(product_id) );''') -Uncomment all of this if you want to use your own DB

#Function for adding a product
def add_product():
    name = input("Name: ")
    category = input("Category: ")
    price = float(input("Price: "))
    db.execute('''INSERT INTO products(name, category, price) 
               VALUES (?, ?, ?);''', (name, category, price))
    db.commit()

#Function for adding a new client
def add_user():
    f_name = input("First name: ")
    l_name = input("Last name: ")
    email = input("Email: ")
    db.execute('''INSERT INTO customers(first_name, last_name, email) 
               VALUES (?, ?, ?);''', (f_name, l_name, email))
    db.commit()

#Function for making an order
def add_order():
    customer_id = int(input("Customer ID: "))
    product_id = int(input("Product ID: "))
    quantity = int(input("Quantity: "))
    order_date = datetime.datetime.now().replace(microsecond=0)
    db.execute('''INSERT INTO orders(customer_id, product_id, quantity, order_date)
               VALUES (?, ?, ?, ?);''', (customer_id, product_id, quantity, order_date))
    db.commit()

#Function for showing the total income
def income():
    info = db.execute('''SELECT SUM(o.quantity * p.price) 
               FROM orders o 
               INNER JOIN products p ON p.product_id == o.product_id;''')
    print(info.fetchone())

#Function for showing the number of orders for each client
def orders_by_customer():
    info = db.execute('''SELECT c.first_name, COUNT(o.order_id) 
                      FROM orders o 
                      INNER JOIN customers c ON o.customer_id == c.customer_id
                      GROUP BY c.first_name;''')
    print(info.fetchall())

#Function for showing the average order price
def avg_order_price():
    info = db.execute('''SELECT AVG(o.quantity * p.price)
                      FROM orders o
                      INNER JOIN products p ON o.product_id == p.product_id;''')
    print(info.fetchone())

#Function for showing the category with the most products
def popular_category():
    info = db.execute('''SELECT p.category, COUNT(o.order_id) AS order_count
                      FROM orders o
                      INNER JOIN products p ON o.product_id == p.product_id
                      GROUP BY p.category
                      ORDER BY order_count DESC;''')
    print(info.fetchone())

#Function for showing total quantity of products in each category
def category_quantity():
    info = db.execute('''SELECT COUNT(p.product_id) as amount, p.category 
                      FROM products p 
                      GROUP BY category
                      ORDER BY amount DESC;''')
    print(info.fetchall())

#Function for increasing the price of all products in selected category by 10%
def update_price():
    category = input("Category: ")
    db.execute('''UPDATE products
               SET price = price * 1.1
               WHERE category == (?)''', (category,))
    db.commit()

#main loop
while True:
    print('''
Select an option:
1 - Add a product
2 - Add a client
3 - Order an item
4 - View total income
5 - View the number of orders for each client
6 - View average order price
7 - View the most popular category
8 - View total quantity of products for each category
9 - Update prices by 10%
0 - Exit''')
    
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
        case 7:
            popular_category()
        case 8:
            category_quantity()
        case 9: 
            update_price()
