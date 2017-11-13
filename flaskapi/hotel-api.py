from flask import Flask, jsonify, request
from flask_mysqldb import MySQL 
import MySQLdb
import string
import random
import datetime

# pip install virtualenv
# venv/bin/activate
# pip install flask
# pip install flask-mysqldb

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel_booking'

mysql = MySQL(app)

# Helper
def id_generator(size, chars=string.ascii_uppercase+string.digits):
	return ''.join(random.choice(chars) for _ in range (size))

def generate_date():
	return datetime.datetime.now()


# Book
@app.route('/book/list', methods = ['GET'])
def list_book():
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT * FROM book''')
	rv = cur.fetchall()
	return jsonify(rv)

@app.route('/book/create', methods = ['POST'])
def create_book():
	if request.method == "POST":
		customer_id = request.form['customer_id']
		paid_price = request.form['paid_price']
		room_id = request.form['type']
		amount = request.form['amount']
		worker_id = request.form['worker_id']
		book_id = id_generator(12)
		transaction_id = id_generator(16)
		date = generate_date()

		cur = mysql.connection.cursor()
		queryCreate = '''INSERT INTO book (id, customer_id, paid_price, type, amount, worker_id) VALUES ('%s', %s, %s, '%s', %s, %s)''' % (book_id, customer_id, paid_price, room_id, amount, worker_id)
		cur.execute(queryCreate)
		queryRoom = '''UPDATE room SET stock = stock - %s WHERE type = '%s' ''' % (amount, room_id)
		cur.execute(queryRoom)		
		queryTransaction = '''INSERT INTO transaction (id, book_id, amount, date) VALUES ('%s', '%s', %s, '%s')''' % (transaction_id, book_id, paid_price, date)
		cur.execute(queryTransaction)
		mysql.connection.commit()
		return ''

@app.route('/book/check/<book_id>')
def check_booking(book_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT * FROM book WHERE (id = '%s')''' % book_id ) 
	rv = cur.fetchall()
	return jsonify(rv)

# Room
@app.route('/room/list', methods = ['GET'])
def list_room():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM room''')
	rv = cur.fetchall()
	return jsonify(rv)

@app.route('/room/create', methods = ['POST'])
def create_room():
	if request.method == "POST":
		type = request.form['type']
		size = request.form['size']
		stock = request.form['stock']
		price = request.form['price']
		cur = mysql.connection.cursor()
		queryCreate = '''INSERT INTO room (type, size, stock, price) VALUES ('%s', '%s', %s, %s)''' % (type, size, stock, price)
		cur.execute(queryCreate)
		mysql.connection.commit()
		return ''


@app.route('/room/check/<room_id>')
def check_availability(room_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT stock FROM room WHERE (type = '%s')''' % room_id ) 
	rv = cur.fetchall()
	if rv[0]['stock'] > 0:
		return "Available"
	else:
		return "Not Available"

# Transaction
@app.route('/transaction/check/<transaction_id>')
def check_transaction(transaction_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT * FROM transaction WHERE (id = '%s')''' % transaction_id ) 
	rv = cur.fetchall()
	return jsonify(rv)

@app.route('/transaction/pay', methods = ['POST'])
def add_payment():
	if request.method == "POST":
		book_id = request.form['book_id']
		paid_price = request.form['paid_price']
		transaction_id = id_generator(16)
		date = generate_date()

		cur = mysql.connection.cursor()
		queryBook = '''UPDATE book SET paid_price = paid_price + %s WHERE id = '%s' ''' % (paid_price, book_id)
		cur.execute(queryBook)
		queryTransaction = '''INSERT INTO transaction (id, book_id, amount, date) VALUES ('%s', '%s', %s, '%s')''' % (transaction_id, book_id, paid_price, date)
		cur.execute(queryTransaction)
		mysql.connection.commit()
		return ''	

# Customer
@app.route('/customer/check/<customer_id>')
def check_customer(customer_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT * FROM customer WHERE (id = '%s')''' % customer_id ) 
	rv = cur.fetchall()
	return jsonify(rv)

@app.route('/customer/create', methods = ['POST'])
def create_customer():
	if request.method == "POST":
		name = request.form['name']

		cur = mysql.connection.cursor()
		queryCreate = '''INSERT INTO customer (name) VALUES ('%s')''' % (name)
		cur.execute(queryCreate)
		mysql.connection.commit()
		return ''

# Worker
@app.route('/worker/check/<worker_id>')
def check_worker(worker_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT * FROM worker WHERE (id = '%s')''' % worker_id ) 
	rv = cur.fetchall()
	return jsonify(rv)

@app.route('/worker/create', methods = ['POST'])
def create_worker():
	if request.method == "POST":
		name = request.form['name']
		date = generate_date()
		cur = mysql.connection.cursor()
		query = '''INSERT INTO worker (name, last_login) VALUES ('%s', '%s')''' % (name, date)
		cur.execute(query)
		mysql.connection.commit()
		return ''

@app.route('/worker/login', methods = ['POST'])
def login_worker():
	if request.method == "POST":
		worker_id = request.form['worker_id']
		date = generate_date()
		cur = mysql.connection.cursor()
		query = '''UPDATE worker SET last_login = '%s' WHERE id = %s ''' % (date, worker_id)
		cur.execute(query)
		mysql.connection.commit()
		return ''

if __name__ == '__main__':
	app.run()

