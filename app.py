from flask import Flask, render_template, url_for, redirect, request, flash
from flask_modus import Modus

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
if __name__ == "__main__":
    app.run(port=4001, debug=True)
