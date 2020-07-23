from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://doc_manager:GetMyDocNumbers789@localhost/DocumentNumbers'
app.config['SECRET_KEY'] = '135d473ff2af445988f0a4be01a5b77c'
db = SQLAlchemy(app)

from document_app import routes