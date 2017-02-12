from flask import Flask, render_template, url_for, redirect, request, flash

app = Flask(__name__)

@app.route('/')
def root():
	return redirect(url_for('index'))

@app.route('/home')
def index():
	return render_template('index.html')

@app.route('/representative', methods=["GET", "POST"])
def representative():

	print("representation page")
	if request.method == "POST":
		return render_template('rep.html', first=request.form['first'], last=request.form['last'], city=request.form['city'])

	else:
		pass

@app.route('/participant', methods=["POST"])
def participant():
	print("participation page")

@app.route('/<lastname>')
def rep():
	pass

    
if __name__ == "__main__":
    app.run(port=4001, debug=True)
