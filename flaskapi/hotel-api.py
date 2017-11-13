from flask import Flask, redirect, url_for, request
from flask_mysqldb import MySQL 

# pip install virtualenv
# venv/bin/activate
# pip install flask
# pip install flask-mysqldb

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel_booking'

mysql = MySQL(app)

@app.route('/')
def init():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM book''')
	rv = cur.fetchall()
	return str(rv)

@app.route('/hello/<name>')
def hello_world(name):
	return "Hello %s!" % name

@app.route('/book/create', methods = ['POST'])
def create_book():
	if request.method == "POST":
		user = request.form['name']
		return "%s" % user
	else:
		return 0

if __name__ == '__main__':
	app.run()

