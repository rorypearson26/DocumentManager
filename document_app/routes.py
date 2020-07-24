from flask import render_template, redirect, url_for, flash
from document_app import app
from document_app.models import DocumentNumber, Project, DocumentType
from document_app.forms import CreateNumberForm, CreateProjectForm, CreateDocTypeForm


@app.route('/', methods=["POST", "GET"])
def home():
    doc_num_query = DocumentNumber.query.order_by(DocumentNumber.creation_date.desc()).all()

    form = CreateNumberForm()
    if form.validate_on_submit():
        new_doc = CreateNumberForm.add_doc_number(form)
        flash(f"Document number: {new_doc.doc_name}"
              f" created with description {new_doc.description}", "success")
        return redirect(url_for('home'))
    else:
        flash_errors(form)
        return render_template("index.html", form=form, doc_nums=doc_num_query)


@app.route('/projects', methods=["POST", "GET"])
def projects():
    project_query = Project.query.order_by(Project.creation_date.desc()).all()
    form = CreateProjectForm()

    if form.validate_on_submit():
        project = CreateProjectForm.add_project(form)
        flash(f"Project: {project.name}"
              f" created with description {project.description}", "success")
        return redirect(url_for('projects'))
    else:
        flash_errors(form)
    return render_template("projects.html", form=form, projects=project_query)


@app.route('/doctypes', methods=["POST", "GET"])
def doc_types():
    doc_type_query = DocumentType.query.order_by(DocumentType.initials).all()
    form = CreateDocTypeForm()

    if form.validate_on_submit():
        doc_type = CreateDocTypeForm.add_doc_type(form)
        flash(f"Document Type: {doc_type.name}"
              f" created with initials {doc_type.initials}", "success")
        return redirect(url_for('doc_types'))
    else:
        flash_errors(form)
    return render_template("documenttypes.html", form=form, doc_types=doc_type_query)


def flash_errors(form):
    """Flashes form errors and displayed as warning"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error), 'warning')
