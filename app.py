from flask import Flask, render_template, url_for, redirect, request, flash

app = Flask(__name__)

@app.route('/')
def root():
	return redirect(url_for('index'))

@app.route('/home')
def index():
	return render_template('index.html')

@app.route('/representative/<name>')
def representative():
	pass

    
if __name__ == "__main__":
    app.run(port=4001, debug=True)
