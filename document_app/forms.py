from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy.sql import func
from document_app.models import DocumentNumber, project_query, doc_type_query
from document_app import db

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

        new_doc = self.new_doc_number()
        db.session.add(new_doc)
        db.session.commit()
        return new_doc

