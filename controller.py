import requests
import json
import connection
import random
import uuid
class Main:
    def read_api(self):
        global url
        dbCalls = DbCalls()
        dbCalls.table_creation(self.connect())
        for item in params_subject:
class DbCalls(Main):
    def __int__(self, cursor):
        self.cursor = cursor
        self.main = Main()
    def drop_if_exists(self, cursor):
        drop_book = "DROP TABLE IF EXISTS Book"
        drop_bookInfo = "DROP TABLE IF EXISTS BookInfo"
        drop_VolumeInfo = "DROP TABLE IF EXISTS VolumeInfo"
        drop_publish = "DROP TABLE IF EXISTS Publish"
        drop_IndustryIdentifier = "DROP TABLE IF EXISTS IndustryIdentifier"
        drop_saleInfo = "DROP TABLE IF EXISTS SaleInfo"

        cursor.execute(drop_IndustryIdentifier)
        cursor.execute(drop_saleInfo)
        cursor.execute(drop_publish)
        cursor.execute(drop_VolumeInfo)
        cursor.execute(drop_bookInfo)
        cursor.execute(drop_book)
    def table_creation(self, cursor):

        self.drop_if_exists(cursor)
        cursor.execute(
            "CREATE TABLE Book "
            "(bookId varchar(255) NOT NULL, "
            "bookCode varchar(255), "
            "type varchar(30), "
            "totalItems int, "
            "PRIMARY KEY(bookId))"
        )

        cursor.execute(
            "CREATE TABLE BookInfo "
            "(bookInfoId varchar(255) NOT NULL, "
            "etag varchar(255), "
            "selfLink varchar(255), "
            "language varchar(30), "
            "isAvailablePDF varchar(10), "
            "bookId varchar(255), "
            "PRIMARY KEY(bookInfoId), "
            "FOREIGN KEY (bookId) REFERENCES Book(bookId))"
        )
        cursor.execute(
            "CREATE TABLE VolumeInfo "
            "(vId varchar(255) NOT NULL, "
            "title varchar(255), "
            "subtitle varchar(1000), "
            "publishedDate varchar(255), "
            "bookId varchar(255), "
            "PRIMARY KEY(vId), "
            "FOREIGN KEY (bookId) REFERENCES Book(bookId))"
        )

        cursor.execute(
            "CREATE TABLE Publish "
            "(pId varchar(255) NOT NULL, "
            "publisher varchar(255), "
            "publishedDate varchar(255), "
            "description varchar(5000), "
            "bookId varchar(255), "
            "PRIMARY KEY (pId),"
            "FOREIGN KEY (bookId) REFERENCES Book(bookId))"
        )

        cursor.execute(
            "CREATE TABLE SaleInfo "
            "(sId varchar(255) NOT NULL, "
            "country varchar(255), "
            "saleAbility varchar(255), "
            "bookId varchar(255), "
            "isEbook varchar(5), "
            "PRIMARY KEY (sId), "
            "FOREIGN KEY (bookId) REFERENCES BookInfo(bookId))"
        )

        cursor.execute(
            "CREATE TABLE IndustryIdentifier "
            "(industryId varchar(255) NOT NULL, "
            "type varchar(255), "
            "identifier varchar(255), "
            "bookId varchar(255), "
            "PRIMARY KEY (industryId), "
            "FOREIGN KEY (bookId) REFERENCES BookInfo(bookId))"
        )
    def get_params(self, new_data, i):
        bookId = str(uuid.uuid4())
        totalItem = random.randint(1, 100)
        etag = main.validate_string(new_data[i]["etag"])
        selfLink = main.validate_string((new_data[i]["selfLink"]))
        language = main.validate_string(new_data[i]["volumeInfo"]["language"])
        isAvailablePDF = main.validate_string(
            new_data[i]["accessInfo"]["pdf"]["isAvailable"]
        )
        vId = str(uuid.uuid4())
        title = main.validate_string(new_data[i]["volumeInfo"]["title"])
        try:
            subtitle = main.validate_string(new_data[i]["volumeInfo"]["subtitle"])
        except:
            subtitle = "null"

