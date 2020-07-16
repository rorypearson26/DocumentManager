from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://doc_manager:GetMyDocNumbers789@localhost/DocumentNumbers'
db = SQLAlchemy(app)

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(100), unique=False, nullable=False,)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class DocumentType(db.Model):
    __tablename__ = 'document_type'
    id = db.Column(db.Integer, primary_key=True)
    initials = db.Column(db.String(2), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False,)

class DocumentNumber(db.Model):
    __tablename__ = 'document_number'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    doc_type_id = db.Column(db.Integer, db.ForeignKey('document_type.id'), nullable=False)
    doc_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=False,)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("projects", test_content=user))
    else:
        return render_template("index.html", content="This is the homepage")
@app.route('/projects/<test_content>')
def projects(test_content):
    return render_template("projects.html", content=test_content)

@app.route('/doctypes')
def doc_types():
    return render_template("documenttypes.html", content="Here are the doc types")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

