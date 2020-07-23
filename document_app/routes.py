from flask import render_template, redirect, url_for, flash
from document_app import app
from document_app.models import DocumentNumber
from document_app.forms import CreateNumberForm

@app.route('/', methods=["POST", "GET"])
def home():
    doc_nums = DocumentNumber.query.order_by(DocumentNumber.creation_date.desc()).all()

    form = CreateNumberForm()
    if form.validate_on_submit():
        new_doc = CreateNumberForm.add_doc_number(form)
        flash(f"Document number: {new_doc.doc_name} created with description {new_doc.description}", "success")
        return redirect(url_for('home'))
    else:
        flash_errors(form)
        return render_template("index.html", form=form, doc_nums=doc_nums)

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/doctypes')
def doc_types():
    return render_template("documenttypes.html", content="Here are the doc types")

def flash_errors(form):
    """Flashes form errors and displayed as warning"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error), 'warning')