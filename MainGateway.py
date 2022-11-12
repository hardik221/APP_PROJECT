import uuid
import random
from connection import Connector
from prettytable import PrettyTable

global db
class TDG():
    def __init__(self):
        c = Connector()
        self.db = c.create_connection()
    def validate_string(self, val=""):
        if val != "":
            if type(val) is int:
                # for x in val:
                #   print(x)
                return str(val).encode("utf-8")
            else:
                return val
        else:
            return ""

    def checkTableExists(self, cursor):
        sql = "SHOW TABLES LIKE 'BookType'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

    def createTables(self, cursor):

        # create BookType Table
        cursor.execute(
            "CREATE TABLE BookType "
            "(id varchar(255) NOT NULL, "
            "bookType varchar(255),"
            "PRIMARY KEY(id))"
        )
        # create Book Table
        cursor.execute(
            "CREATE TABLE Book "
            "(id varchar(255) NOT NULL, "
            "title varchar(255), "
            "pageCount int, "
            "isEbook varchar(5), "
            "typeId varchar(255), "
            "PRIMARY KEY(id),"
            "FOREIGN KEY(typeId) REFERENCES BookType(id))"
        )

        # create Publish Table
        cursor.execute(
            "CREATE TABLE Publish "
            "(id varchar(255) NOT NULL, "
            "publisher varchar(255), "
            "publishedDate varchar(255), "
            "description varchar(1500), "
            "bookId varchar(255), "
            "PRIMARY KEY(id), "
            "FOREIGN KEY (bookId) REFERENCES Book(id))"
        )

    def insertBookType(self, typeId, bookType, cursor):
        cursor.execute(
            "INSERT INTO BookType (id, bookType) VALUES (%s, %s)",
            (typeId, bookType),
        )
        self.db.commit()

    def insertBook(self, bookId, title, pageCount, isEbook, typeId, cursor):
        cursor.execute(
            "INSERT INTO Book (id, title, pageCount, isEbook, typeId) VALUES (%s, %s, %s, %s, %s)",
            (bookId, title, pageCount, isEbook, typeId),
        )
        self.db.commit()

    def insertPublish(self, pId, publisher, publishedDate, description, bookId, cursor):
        cursor.execute(
            "INSERT INTO Publish (id, publisher, publishedDate, description, bookId) VALUES (%s, %s, %s, %s, %s)",
            (pId, publisher, publishedDate, description, bookId),
        )
        self.db.commit()
    def get_params(self, new_data, i):
        bookId = str(uuid.uuid4())[:8]

        title = self.validate_string(new_data[i]["volumeInfo"]["title"])
        try:
            pageCount = self.validate_string(new_data[i]["volumeInfo"]["pageCount"])
        except:
            pageCount = random.randint(100, 300)

        try:
            publishedDate = self.validate_string(
                new_data[i]["volumeInfo"]["publishedDate"]
            )
        except:
            publishedDate = "null"

        pId = str(uuid.uuid4())[:8]
        try:
            publisher = self.validate_string(new_data[i]["volumeInfo"]["publisher"])
        except:
            publisher = "Concordia University"

        try:
            description = self.validate_string(
                new_data[i]["volumeInfo"]["description"][:100]
            )
        except:
            description = "No description available"

        isEbook = self.validate_string(new_data[i]["saleInfo"]["isEbook"])

        return bookId, title, pageCount, isEbook, pId, publisher, publishedDate, publishedDate, description

    def data_insertion_into_table(self, new_data, bookType, cursor):

        # insert data into BookType Table
        typeId = str(uuid.uuid4())[:8]
        self.insertBookType(typeId, bookType, cursor)

        for i in range(len(new_data)):
            bookId, title, pageCount, isEbook, pId, publisher, publishedDate, publishedDate, description = self.get_params(new_data, i)

            sql = f"SELECT id FROM BookType where bookType = '{bookType}'"
            cursor.execute(sql)
            typeId = cursor.fetchone()[0]

            # insert data into Book Table
            self.insertBook(bookId, title, pageCount, isEbook, typeId, cursor)

            # sql = f"SELECT bookId FROM Book where title = '{title}'"
            # cursor.execute(sql)
            #
            # print("----->", type(bookId))
            # insert data into Publish Table
            self.insertPublish(pId, publisher, publishedDate, description, bookId, cursor)

    def findAll(self, cursor, tableName):

        sql = f"SELECT * FROM {tableName}"
        cursor.execute(sql)
        row_data = cursor.fetchall()
        return row_data

    def findById(self, cursor, tableName, var, id):

        sql = f"SELECT * FROM {tableName} where {var} = '{id}'"
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    def update(self, cursor, tableName, var, new_var, id):
        sql = f"UPDATE {tableName} SET {var}='{new_var}' WHERE id = '{id}'"
        cursor.execute(sql)
        self.db.commit()

    def deleteById(self, cursor, tableName, id):
        sql = f"DELETE FROM {tableName} where id = '{id}'"
        cursor.execute(sql)
        self.db.commit()

    def display(self, cursor, data, tableName):
        if len(data) == 0:
            print("Data doesn't exist.")

        cursor.execute(f"SHOW columns FROM {tableName}")
        columns = [column[0] for column in cursor.fetchall()]

        t = PrettyTable(columns)

        for tuples in data:
            t.add_row(list(tuples))
        print(t)