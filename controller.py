import requests
import json
import connection
import random
import uuid

params_subject = ['love', 'feminism', 'inspirational', 'authors', 'fiction', 'poetry', 'fantasy', 'romance']
class Main:
    def read_api(self):
        global url
        dbCalls = DbCalls()
        dbCalls.table_creation(self.connect())
        for item in params_subject:
            url = f'https://www.googleapis.com/books/v1/volumes?q={str(item)}:keyes&key=AIzaSyCB4mblXymeFZnTJKzp409fWKh8QC8Ty5Y&maxResults=10'

            api_result = requests.get(url)

            api_response = api_result.json()
            self.write_data(api_response)
            data = self.read_data()
            dbCalls.data_insertion_into_table(data, self.connect())
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
        # connect to MySQL
        cursor = connection.db1.cursor()
        return cursor
    def read_data(self):
        f = open("api_data.json", "r")
        new_data = json.loads(f.read())
        return new_data['items']
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

        try:
            publishedDate = main.validate_string(
                new_data[i]["volumeInfo"]["publishedDate"]
            )
        except:
            publishedDate = "null"

        pId = str(uuid.uuid4())
        try:
            publisher = main.validate_string(new_data[i]["volumeInfo"]["publisher"])
        except:
            publisher = "Concordia University"

        try:
            description = main.validate_string(
                new_data[i]["volumeInfo"]["description"]
            )
        except:
            description = "No description available"

        sId = str(uuid.uuid4())
        countryChoice = ["CA", "US", "IN", "GE", "UK", "AU"]
        country = random.choice(countryChoice)
        saleAbility = main.validate_string(new_data[i]["saleInfo"]["saleability"])
        isEbook = main.validate_string(new_data[i]["saleInfo"]["isEbook"])
        industryId = str(uuid.uuid4())
        typeOfIdentifier = ""
        identifier = ""
        try:
            for j in range(len(new_data[i]["volumeInfo"]["industryIdentifiers"])):
                try:
                    typeOfIdentifier += (
                            main.validate_string(
                                new_data[i]["volumeInfo"]["industryIdentifiers"][j]["type"]
                            ) + ", "
                    )
                    identifier += (
                            main.validate_string(
                                new_data[i]["volumeInfo"]["industryIdentifiers"][j]["identifier"]
                            ) + ", "
                    )
                except:
                    typeOfIdentifier += ""
                    identifier += ""
        except:
            pass

        if typeOfIdentifier != "":
            typeOfIdentifier = typeOfIdentifier[:-2]
            identifier = identifier[:-2]

        return bookId, totalItem, etag, selfLink, language, isAvailablePDF, vId, title, subtitle, publishedDate, pId, publisher, publishedDate, description, sId, country, saleAbility, isEbook, industryId, typeOfIdentifier, identifier
    def data_insertion_into_table(self, new_data, cursor):
        # parse json data to SQL insert

        bookId = str(uuid.uuid4())
        type = url.split("?")[1].split("=")[1].split(":")[0]
        totalItems = random.randint(1, 40)

        cursor.execute(
            "INSERT INTO Book (bookId, type, totalItems) VALUES (%s, %s, %s)",
            (bookId, type, totalItems),
        )
        connection.db1.commit()

        for i in range(len(new_data)):
            bookId, totalItem, etag, selfLink, language, isAvailablePDF, vId, title, subtitle, publishedDate, pId, publisher, publishedDate, description, sId, country, saleAbility, isEbook, industryId, typeOfIdentifier, identifier = self.get_params(
                new_data, i)
            sql = f"SELECT bookId FROM book where type = '{type}'"
            cursor.execute(sql)


            bookId = cursor.fetchone()[0]
            bookInfoId = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO BookInfo (bookInfoId, etag, selfLink, language, isAvailablePDF, bookId) VALUES (%s, %s, %s, %s, %s, %s)",
                (bookInfoId, etag, selfLink, language, isAvailablePDF, bookId),
            )

            cursor.execute(
                "INSERT INTO VolumeInfo (vId, title, subtitle, publishedDate, bookId) VALUES (%s, %s, %s, %s, %s)",
                (vId, title, subtitle, publishedDate, bookId),
            )

            cursor.execute(
                "INSERT INTO Publish (pId, publisher, publishedDate, description, bookId) VALUES (%s, %s, %s, %s, %s)",
                (pId, publisher, publishedDate, description[:1000], bookId),
            )

            cursor.execute(
                "INSERT INTO SaleInfo (sId, country, saleAbility, isEbook, bookId) VALUES (%s, %s, %s, %s, %s)",
                (sId, country, saleAbility, isEbook, bookId),
            )

            cursor.execute(
                "INSERT INTO IndustryIdentifier (industryId, type, identifier, bookId) VALUES (%s, %s, %s, %s)",
                (industryId, typeOfIdentifier, identifier, bookId),
            )

        connection.db1.commit()
        print("Data inserted successfully into all the table")

if __name__ == "__main__":
    main = Main()

    # Read API data into JSON
    main.read_api()
