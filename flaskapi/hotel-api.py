from flask import Flask, jsonify, request
from flask_mysqldb import MySQL 
import MySQLdb

# pip install virtualenv
# venv/bin/activate
# pip install flask
# pip install flask-mysqldb

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel_booking'

mysql = MySQL(app)

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
		cur = mysql.connection.cursor()
		queryCreate = '''INSERT INTO book (customer_id, paid_price, type, amount) VALUES (%s, %s, '%s', %s)''' % (customer_id, paid_price, room_id, amount)
		cur.execute(queryCreate)
		queryUpdate = '''UPDATE room SET stock = stock - %s''' % (amount)
		cur.execute(queryUpdate)
		mysql.connection.commit()
		return ""

# Room
@app.route('/room/list', methods = ['GET'])
def list_room():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM room''')
	rv = cur.fetchall()
	return jsonify(rv)

@app.route('/room/check/<room_id>')
def check_availability(room_id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('''SELECT stock FROM room WHERE (type = '%s')''' % room_id ) 
	rv = cur.fetchall()
	if rv[0]['stock'] > 0:
		return "Available"
	else:
		return "Not Available"
if __name__ == '__main__':
	app.run()

