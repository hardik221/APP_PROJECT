from unittest import TestCase
import mysql.connector
from mysql.connector import errorcode
from mock import patch
import utils

MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "book"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"

class MockDb(TestCase):

    @classmethod
    def setUpClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT
        )
        cursor = cnx.cursor(dictionary=True)

        # drop database if it already exists
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cursor.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            print("{}{}".format(MYSQL_DB, err))

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_DB))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cnx.database = MYSQL_DB


        try:
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

            cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("test_table already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        try:
            cursor.execute("INSERT INTO bookType (id, bookType) "
                           "VALUES ('1', 'love'), ('2', 'fantasy')")
            cursor.execute(
                "INSERT INTO book (id, title, pageCount, isEbook, typeId) "
                "VALUES "
                "('11', 'Three series - 1', 500, 'true', '1'), "
                "('12', 'Three series - 2', 340, 'false', '2'), "
                "('13', 'Three series-3', 780, 'true', '1')")
            cursor.execute(
                "INSERT INTO publish (id, publisher, publishedDate, description, bookId) "
                "VALUES "
                "('21', 'Hardik', '1996', 'description 1', '11'), "
                "('22', 'Jeet', '1998', 'description 2', '12')")

            cnx.commit()
        except mysql.connector.Error as err:
            print("Data insertion to test_table failed \n" + err)
        cursor.close()
        cnx.close()

        testconfig ={
            'host': MYSQL_HOST,
            'user': MYSQL_USER,
            'password': MYSQL_PASSWORD,
            'database': MYSQL_DB
        }
        cls.mock_db_config = patch.dict(utils.config, testconfig)

    @classmethod
    def tearDownClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = cnx.cursor(dictionary=True)

        # drop test database
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database {} does not exists. Dropping db failed".format(MYSQL_DB))
        cnx.close()

