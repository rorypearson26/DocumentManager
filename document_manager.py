import mysql.connector

class MyDocName:
    length = 4
    def __init__(self, project_number, doc_type, doc_number):
        self.project_number = project_number
        self.doc_type = doc_type
        self.doc_number = doc_number
        self.name_formatter()

    def name_formatter(self):
        """Function to format number together"""
        project_number = MyDocName.number_padder(self.project_number, 4)
        doc_number = MyDocName.number_padder(self.doc_number, 4)
        doc_name = "".join([str(project_number), "-", str(self.doc_type), "-", str(doc_number)])
        self.full_name = doc_name


    def number_padder(input_string, length):
        """Function to pad out strings properly with leading zeros"""
        return str(input_string).zfill(length)

class MyDB:
    """Class to create and use a database object"""
    def __init__(self, args):
        """Create the attributes needed for connection to the database"""
        self.host = args[0]
        self.user = args[1]
        self.password = args[2]
        self.db_name = args[3]
        self.connect_me()

    def connect_me(self):
        """Function to establish connection with the database and set up cursor"""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.db_name
        )
        self.my_cursor = self.connection.cursor()


# db = MyDB(['localhost', 'doc_manager', 'GetMeDocNumbers789', 'test_doc_db'])
# my_doc = MyDocName(1, 'dp', 1)
# #db.connect()
# #db.cursor()
# db.my_cursor.execute('SELECT * FROM doc_names')
# myres = db.my_cursor.fetchall()
# print(my_doc.full_name)
# print(myres)
# db.connection.close()
# db.my_cursor.close()