import mysql.connector as mysql

# Authenticators
host = "localhost"
username = "root"
password = "Hardik@123"

# mysql connection
try:
    db = mysql.connect(host=host, username=username, password=password)
    print("Connected to mysql server successfully!!")

    # Creating a database
    try:
        command_handler = db.cursor()
        command_handler.execute("CREATE DATABASE books")
        print("books database has been created")
    except Exception as e:
        # Connecting to an existing database
        print("Could not create database. Database with given name already exists")
        print("Connecting with the database ...")
        db1 = mysql.connect(host=host, username=username, password=password, database="books")
        print("Connected to books database")

except Exception as e:
    print(e)
    print("Failed to connected....")





