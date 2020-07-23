from datetime import datetime
from document_app import db

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
    doc_name = db.Column(db.String(12), nullable=False)
    description = db.Column(db.String(100), nullable=False,)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    doc_type = db.relationship("DocumentType", backref="doc_name")
    project = db.relationship("Project", backref="doc_name")

    def __init__(self, project_id, doc_type_id, doc_number, description):
        self.project_id = project_id
        self.doc_type_id = doc_type_id
        self.doc_number = doc_number
        self.description = description
        self.doc_name = self.doc_name_maker()

    @staticmethod
    def zero_padder(input_str, length):
        """Function to pad out strings properly with leading zeros"""
        return str(input_str).zfill(length)

    def doc_name_maker(self):
        """Function to construct the full document name"""
        project = self.zero_padder(self.project_id, 4)
        doc_number = self.zero_padder(self.doc_number, 4)
        doc_type = DocumentType.query.filter(DocumentType.id == self.doc_type_id).all()[0]
        doc_name = "".join([str(project), "-", str(doc_type.initials), "-", str(doc_number)])
        return doc_name

def project_query():
    return Project.query.order_by(Project.id)

def doc_type_query():
    return DocumentType.query.order_by(DocumentType.id)
