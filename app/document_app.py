from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://doc_manager:GetMyDocNumbers789@localhost/DocumentNumbers'
app.config['SECRET_KEY'] = '135d473ff2af445988f0a4be01a5b77c'
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
    form = CreateNumberForm()
    if form.validate_on_submit():
        flash(f"Document number created", "success")
        return redirect(url_for('home'))
    else:
        flash_errors(form)
        return render_template("index.html", form=form)

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/doctypes')
def doc_types():
    return render_template("documenttypes.html", content="Here are the doc types")

def project_query():
    return Project.query.order_by(Project.id)

def doc_type_query():
    return DocumentType.query.order_by(DocumentType.id)

def flash_errors(form):
    """Flashes form errors and displayed as warning"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error), 'warning')

def doc_name_maker(Document):
    """Function to construct the full document name"""
    project = zero_padder(Document.project, 4)
    doc_number = zero_padder(Document.doc_number, 4)
    Document.doc_name = "".join([str(project), "-", str(Document.doc_type), "-", str(doc_number)])
    return Document

class CreateNumberForm(FlaskForm):
    """Define fields required for creating a new number form"""

    description = StringField(label='Description',
                              render_kw={"placeholder": "Fill out sensible name",
                                         "maxlength": 40},
                              validators=[DataRequired(), Length(min=10, max=40)])
    project = QuerySelectField(query_factory=project_query, get_label="name")
    doc_type = QuerySelectField(query_factory=doc_type_query, get_label="initials")
    submit = SubmitField('Create')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

