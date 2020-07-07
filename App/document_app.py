from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "This is Rory's homepage"

@app.route('/search')
def search():
    return '<h2> This is an alternative</h2>'

if __name__ == "__main__":
    app.run(debug=True)