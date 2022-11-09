import requests
import json
import pymysql
import connection
import random
import uuid
params_subject = ['love', 'feminism', 'inspirational', 'authors', 'fiction', 'poetry', 'fantasy', 'romance']

url = f'https://www.googleapis.com/books/v1/volumes?q={str(random.choice(params_subject))}:keyes&key=AIzaSyCB4mblXymeFZnTJKzp409fWKh8QC8Ty5Y&maxResults=40'

class Main:
    def read_api(self):
        global url
        api_result = requests.get(url)

        api_response = api_result.json()
        # api_data = json.dumps(api_response, indent=4)
        # new_data = json.loads(api_data)
        # for i in range(len(new_data)):
        #     print(new_data['items'][i]['id'])
        print("-----", api_response["items"][0])
        return api_response["items"]

    def write_data(self, api_response):
        try:
            # Downloading json data into a file
            data = json.dumps(api_response)
            file = open("api_data.json", "w")
            file.write(data)
            print("API data successfully downloaded!!")
        except:
            print("Error in File creation/ data insertion")

    def connect(self):
        # # connect to MySQL
        # #con = pymysql.connect(host = 'localhost',user = 'root',passwd = '',db = 'test')
        cursor = connection.db1.cursor()
        return cursor

    def read_data(self):
        f = open("api_data.json", "r")
        new_data = json.loads(f.read())
        return new_data

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


class DbCalls(Main):
    def __int__(
        self,
        cursor,
    ):
        self.cursor = cursor
        self.main = Main()

    def table_creation(self, cursor):
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

        cursor.execute(
            "CREATE TABLE Book "
            "(bookId varchar(255) NOT NULL, "
            "type varchar(30), "
            "totalItems int, "
            "PRIMARY KEY(bookId))"
        )

        cursor.execute(
            "CREATE TABLE BookInfo "
            "(bookId varchar(255) NOT NULL, "
            "etag varchar(255), "
            "selfLink varchar(255), "
            "language varchar(30), "
            "isAvailablePDF varchar(10), "
            "PRIMARY KEY(bookId), "
            "FOREIGN KEY (bookId) REFERENCES Book(bookId))"
        )
        cursor.execute(
            "CREATE TABLE VolumeInfo "
            "(vId varchar(255) NOT NULL, "
            "title varchar(255), "
            "subtitle varchar(255), "
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

    def data_insertion_into_table(self, new_data):
        # parse json data to SQL insert
        type = url.split('?')[1].split('=')[1].split(':')[0]
        for i in range(len(new_data)):
            print(new_data['items'][i]['id'], new_data['items'][i]['selfLink'])
            bookId = main.validate_string(new_data['items'][i]['id'])
            totalItem = main.validate_string(new_data['totalItems'])
            cursor.execute("INSERT INTO Book (bookId, type, totalItems) VALUES (%s, %s, %s)", (bookId, type, totalItem))
        print('Data inserted successfully')

        connection.db1.commit()


if __name__ == "__main__":
    # Read API data into JSON
    main = Main()
    json_data = main.read_api()
    # Create a api_data.json file and put downloaded data into that file
    main.write_data(json_data)
    # Connect with DB
    cursor = main.connect()
    # Read data from downloaded file
    data = main.read_data()
    # Table creation
    dbCalls = DbCalls()
    dbCalls.table_creation(cursor)

    # insert data into table
    dbCalls.data_insertion_into_table(data)
