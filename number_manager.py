import mysql.connector

def database_connection():
    """Function to open connection with the document_manager database"""
    mydb = mysql.connector.connect(
        host='localhost',
        user='doc_manager',
        passwd='GetMeDocNumbers789',
        database='test_doc_db'
    )
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM doc_names')
    myresult = mycursor.fetchall()
    print(myresult)


def doc_name_maker(project, doc_type, doc_number):
    """Function to construct the full document name"""
    project = zero_padder(project, 4)
    doc_number = zero_padder(doc_number, 4)
    doc_name = "".join([str(project), "-", str(doc_type), "-", str(doc_number)])
    return doc_name

def zero_padder(input_str, length):
    """Function to pad out strings properly with leading zeros"""
    return str(input_str).zfill(length)

#print(doc_name_maker(1, "DP", 1))
database_connection()