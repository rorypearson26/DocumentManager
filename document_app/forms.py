from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy.sql import func
from document_app.models import DocumentNumber, Project, DocumentType, project_query, doc_type_query
from document_app import db


def check_unique(val_type):
    def _check_unique(form, field):
        """Function to check whether field is unique before inserting to database.
        Returns: TRUE, field is unique in it's column; FALSE, non-unique in it's column."""
        if val_type == "project":

            result = Project.query.filter(Project.name == field.data).all()

        elif val_type == "doc_type":
            result = DocumentType.query.filter(DocumentType.initials == field.data).all()
        else:
            result = "fail"
        print(result)
        if result:
            raise ValidationError(f" \"{field.data}\" already exists in table")

    return _check_unique


class CreateNumberForm(FlaskForm):
    """Define fields required for creating a new number form"""
    description = StringField(label='Description',
                              render_kw={"placeholder": "Fill out sensible name",
                                         "maxlength": 40},
                              validators=[DataRequired(), Length(min=1, max=40)])
    project = QuerySelectField(query_factory=project_query, get_label="name")
    doc_type = QuerySelectField(query_factory=doc_type_query, get_label="initials")
    submit = SubmitField('Create')

    def new_doc_number(self):
        """Function to return the next available number for a
        specific project and document type."""
        project = self.project.data.id
        doc_type = self.doc_type.data.id
        description = self.description.data
        current_max = db.session.query(func.max(DocumentNumber.doc_number)) \
            .filter(DocumentNumber.project_id == project) \
            .filter(DocumentNumber.doc_type_id == doc_type) \
            .all()[0][0]

        if current_max is None:
            doc_number = 1
        else:
            doc_number = current_max + 1

        new_doc = DocumentNumber(project_id=project,
                                 doc_type_id=doc_type,
                                 doc_number=doc_number,
                                 description=description)
        return new_doc

    def add_doc_number(self):
        """Function to add new document number to the database"""
        new_doc = self.new_doc_number()
        db.session.add(new_doc)
        db.session.commit()
        return new_doc


class CreateProjectForm(FlaskForm):
    """Define fields required for creating a new project form"""
    name = StringField(label='Project Name',
                       render_kw={"placeholder": "Short name for project",
                                  "maxlength": 30},
                       validators=[DataRequired(), Length(min=4, max=30), check_unique(val_type="project")])
    description = TextAreaField(label='Project Description',
                                render_kw={"placeholder": "More details (max 100 characters)",
                                           "maxlength": 120},
                                validators=[DataRequired(), Length(min=10, max=120)])
    submit = SubmitField('Create')

    def new_project(self):
        """Function to initialise a new project object based on filled
        out fields."""
        new_project = Project(name=self.name.data,
                              description=self.description.data)
        return new_project

    def add_project(self):
        """Add new project to the database"""
        new_project = self.new_project()
        db.session.add(new_project)
        db.session.commit()
        return new_project


class CreateDocTypeForm(FlaskForm):
    """Define fields required for creating a new document type form"""
    initials = StringField(label='Initials',
                           render_kw={"placeholder": "Two-letter initial",
                                      "maxlength": 2},
                           validators=[DataRequired(), Length(min=2, max=2), check_unique(val_type="doc_type")])
    name = StringField(label='Name',
                           render_kw={"placeholder": "Initials expanded",
                                      "maxlength": 30},
                           validators=[DataRequired(), Length(min=10, max=30)])
    description = TextAreaField(label='Document type description',
                                render_kw={"placeholder": "More details (max 100 characters)",
                                           "maxlength": 100},
                                validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Create')

    def new_doc_type(self):
        """Function to initialise a new document type object based on filled
        out fields."""
        new_doc_type = DocumentType(initials=self.initials.data,
                                    name=self.name.data,
                                    description=self.description.data)
        return new_doc_type

    def add_doc_type(self):
        """Add new document type to the database"""
        new_doc_type = self.new_doc_type()
        db.session.add(new_doc_type)
        db.session.commit()
        return new_doc_type
