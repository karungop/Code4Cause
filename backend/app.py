from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask World!"

@app.route('/about')
def about():
    return "About Page"

if __name__ == '__main__':
    app.run(debug=True)