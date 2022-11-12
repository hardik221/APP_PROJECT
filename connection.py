import mysql.connector as mysql

class Connector:
    db = None
    count = 0
    def create_connection(self):
        # Authenticators
        host = "localhost"
        username = "root"
        password = "root"

        if Connector.count == 0:
        # mysql connection
            try:
                Connector.db = mysql.connect(host=host, username=username, password=password)
                print("Connected to mysql server successfully!!")

                # Creating a database
                try:
                    command_handler = Connector.db.cursor(buffered=True)
                    command_handler.execute("CREATE DATABASE books")
                    print("books database has been created")
                except Exception as e:
                    # Connecting to an existing database
                    print("Database with given name already exists.")
                    print("Connecting with the database ...")
                Connector.db = mysql.connect(host=host, username=username, password=password, database="books")
                print("Connected to books database")

            except Exception as e:
                print(e)
                print("Failed to connected....")
            Connector.count = 1
            print("---->1", Connector.db)
            return Connector.db
        else:
            print("---->2", Connector.db)
            return Connector.db





