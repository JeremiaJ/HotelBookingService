from flask import Flask, redirect, url_for, request
app = Flask(__name__)

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

