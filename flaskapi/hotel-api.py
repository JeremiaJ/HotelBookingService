from flask import Flask, jsonify, request
from flask_mysqldb import MySQL 
import MySQLdb
import string
import random
import datetime

# pip install virtualenv
# virtualenv venv
# venv\scripts\activate
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

def check_room_stock_availability(room_id, requested_stock_amount):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT stock FROM room WHERE (type = '%s')''' % room_id ) 
	rv = cur.fetchall()
	if int(rv[0]['stock']) >= requested_stock_amount:
		return True
	else:
		return False

def check_valid_room_id(room_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT stock FROM room WHERE (type = '%s')''' % room_id ) 
	rv = cur.fetchall()
	if len(rv) > 0:
		return True
	else:
		return False

def check_valid_customer_id(customer_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT id FROM customer WHERE (id = '%s')''' % customer_id ) 
	rv = cur.fetchall()
	if len(rv) > 0:
		return True
	else:
		return False

def check_valid_worker_id(worker_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT id FROM worker WHERE (id = '%s')''' % worker_id ) 
	rv = cur.fetchall()
	if len(rv) > 0:
		return True
	else:
		return False

def get_room_price(room_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT price FROM room WHERE (type = '%s')''' % room_id ) 
	rv = cur.fetchall()
	return int(rv[0]['price'])

@app.route('/book/validate', methods = ['POST'])
def validate_book():
	if request.method == "POST":
		customer_id = request.form['customer_id']
		if check_valid_customer_id(customer_id) == False:
			return 'invalid customer_id', 412
		paid_price = 0
		room_id = request.form['type']
		if check_valid_room_id(room_id) == False:
			return 'invalid room_id', 412
		amount = int(request.form['amount'])
		if amount <= 0:
			return 'invalid amount', 412
		if check_room_stock_availability(room_id, amount) == False:
			return 'not enough stock for room %s' % room_id, 412
		worker_id = request.form['worker_id']
		if check_valid_worker_id(worker_id) == False:
			return 'invalid worker_id', 412
		return 'ok'

@app.route('/book/create', methods = ['POST'])
def create_book():
	if request.method == "POST":
		customer_id = request.form['customer_id']
		if check_valid_customer_id(customer_id) == False:
			return 'invalid customer_id', 412
		paid_price = 0
		room_id = request.form['type']
		if check_valid_room_id(room_id) == False:
			return 'invalid room_id', 412
		amount = int(request.form['amount'])
		if amount <= 0:
			return 'invalid amount', 412
		if check_room_stock_availability(room_id, amount) == False:
			return 'not enough stock for room %s' % room_id, 412
		worker_id = request.form['worker_id']
		if check_valid_worker_id(worker_id) == False:
			return 'invalid worker_id', 412
		book_id = id_generator(12)
		total_price = get_room_price(room_id) * amount
		date = generate_date()

		cur = mysql.connection.cursor()
		queryCreate = '''INSERT INTO book (id, customer_id, paid_price, type, amount, worker_id, total_price) VALUES ('%s', %s, %s, '%s', %s, %s, %s)''' % (book_id, customer_id, paid_price, room_id, amount, worker_id, total_price)
		cur.execute(queryCreate)
		queryRoom = '''UPDATE room SET stock = stock - %s WHERE type = '%s' ''' % (amount, room_id)
		cur.execute(queryRoom)		
		mysql.connection.commit()
		return ''

@app.route('/book/check/<book_id>', methods = ['GET'])
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
def check_valid_transaction_id(transaction_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT id FROM transaction WHERE (id = '%s')''' % transaction_id ) 
	rv = cur.fetchall()
	if len(rv) > 0:
		return True
	else:
		return False

@app.route('/transaction/check/<transaction_id>', methods = ['GET'])
def check_transaction(transaction_id):
	if check_valid_transaction_id(transaction_id) == false:
		return 'invalid transaction_id', 412
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT * FROM transaction WHERE (id = '%s')''' % transaction_id ) 
	rv = cur.fetchall()
	return jsonify(rv)

def check_valid_book_id(book_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT id FROM book WHERE (id = '%s')''' % book_id ) 
	rv = cur.fetchall()
	if len(rv) > 0:
		return True
	else:
		return False

def get_total_price(book_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT total_price FROM book WHERE (id = '%s')''' % book_id ) 
	rv = cur.fetchall()
	return int(rv[0]['total_price'])

@app.route('/transaction/pay', methods = ['POST'])
def add_payment():
	if request.method == "POST":
		book_id = request.form['book_id']
		if check_valid_book_id(book_id) == False:
			return 'invalid book_id', 412
		total_price = get_total_price(book_id)
		transaction_id = id_generator(16)
		date = generate_date()

		cur = mysql.connection.cursor()
		queryTransaction = '''INSERT INTO transaction (id, book_id, amount, date) VALUES ('%s', '%s', %s, '%s')''' % (transaction_id, book_id, 0, date)
		cur.execute(queryTransaction)
		mysql.connection.commit()
		pay_response = {"transaction_id": transaction_id, "total_price": total_price}
		return '''%s,%s''' % (transaction_id, total_price)

def get_book_id(transaction_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT book_id FROM transaction WHERE (id = '%s')''' % transaction_id ) 
	rv = cur.fetchall()
	return rv[0]['book_id']

@app.route('/transaction/success/<transaction_id>', methods = ['GET'])
def success_transaction(transaction_id):
	if check_valid_transaction_id(transaction_id) == False:
		return 'invalid transaction_id', 412
	book_id = get_book_id(transaction_id)
	total_price = get_total_price(book_id)
	date = generate_date()
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	queryBook = '''UPDATE book SET paid_price = %s WHERE id = '%s' ''' % (total_price, book_id)
	cur.execute(queryBook)

	new_transaction_id = id_generator(16)

	queryTransaction = '''INSERT INTO transaction (id, book_id, amount, date) VALUES ('%s', '%s', %s, '%s')''' % (new_transaction_id, book_id, total_price, date)
	cur.execute(queryTransaction)

	mysql.connection.commit()
	rv = cur.fetchall()
	return 'ok'

@app.route('/transaction/fail/<transaction_id>', methods = ['GET'])
def fail_transaction(transaction_id):
	if check_valid_transaction_id(transaction_id) == False:
		return 'invalid transaction_id', 412
	book_id = get_book_id(transaction_id)
	date = generate_date()
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	queryBook = '''UPDATE book SET paid_price = %s WHERE id = '%s' ''' % (-1, book_id)
	cur.execute(queryBook)

	new_transaction_id = id_generator(16)

	queryTransaction = '''INSERT INTO transaction (id, book_id, amount, date) VALUES ('%s', '%s', %s, '%s')''' % (new_transaction_id, book_id, -1, date)
	cur.execute(queryTransaction)

	mysql.connection.commit()
	rv = cur.fetchall()
	return 'ok'

# Customer
@app.route('/customer/check/<customer_id>', methods = ['GET'])
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
@app.route('/worker/check/<worker_id>', methods = ['GET'])
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
	app.run(host= '0.0.0.0')