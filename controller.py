from connection import Connector
import requests
import json
global url
global db
from MainGateway import TDG

params_subject = ['love', 'feminism', 'inspirational', 'authors', 'fiction', 'poetry', 'fantasy', 'romance']

class Main:
    def read_api_and_insert_data(self, tdg):

        for item in params_subject:
            url = f'https://www.googleapis.com/books/v1/volumes?q={str(item)}:keyes&key=AIzaSyCB4mblXymeFZnTJKzp409fWKh8QC8Ty5Y&maxResults=2'
            api_result = requests.get(url)
            api_response = api_result.json()

            self.write_data(api_response)
            data = self.read_data()
            tdg.data_insertion_into_table(data, item, self.connect())

    def write_data(self, api_response):
        try:
            # Downloading json data into a file
            data = json.dumps(api_response)
            file = open("api_data.json", "w")
            file.write(data)

        except:
            print("Error in File creation/ data insertion")

    def connect(self):
        # connect to MySQL
        cursor = db.cursor()
        return cursor

    def read_data(self):
        f = open("api_data.json", "r")
        new_data = json.loads(f.read())
        return new_data['items']



if __name__ == "__main__":
    c = Connector()
    db = c.create_connection()

    tdg = TDG()
    main = Main()
    cursor = db.cursor()

    if tdg.checkTableExists(cursor) == False:
        # Read API data into JSON
        tdg.createTables(cursor)
        main.read_api_and_insert_data(tdg)
        print("*************************************************\n"
              "* Data inserted successfully into all the table *\n"
              "*************************************************")
    else:
        print("Tables are already Exists")

    while True:
        print("Select Task:\n"
              "1. FIND ALL \n"
              "2. FIND BY ID\n"
              "3. UPDATE\n"
              "4. DELETE\n"
              "5. EXIT\n")

        user_input = int(input("Enter Number: "))
        tables = ['bookType', 'book', 'publish']

        match user_input:
            case 1:
                # Fetch All
                print("\nSELECT TABLE: \n"
                      "1. bookType\n"
                      "2. book\n"
                      "3. publish\n")
                tableIndex = int(input("Enter Number: "))
                tableName = tables[tableIndex - 1]

                data = tdg.findAll(cursor, tableName)
                tdg.display(cursor, data, tableName)

            case 2:
                # Fetch By Id
                print("SELECT TABLE: \n"
                      "1. bookType\n"
                      "2. book\n"
                      "3. publish\n")

                tableIndex = int(input("Enter Number: "))
                tableName = tables[tableIndex - 1]

                id1 = input("Enter id number: ")
                cursor.execute(f"SHOW columns FROM {tableName}")
                print([column[0] for column in cursor.fetchall()])
                var = input("Enter field you want to fetch: ")
                data = tdg.findById(cursor, tableName, var, id1)
                tdg.display(cursor, data, tableName)

            case 3:
                # Update By Id
                print("SELECT TABLE: \n"
                      "1. bookType\n"
                      "2. book\n"
                      "3. publish\n")

                tableIndex = int(input("Enter Number: "))
                tableName = tables[tableIndex - 1]
                data = tdg.findAll(cursor, tableName)
                tdg.display(cursor, data, tableName)

                id = input("Enter id number: ")
                cursor.execute(f"SHOW columns FROM {tableName}")
                print([column[0] for column in cursor.fetchall()])

                var = input("Enter field you want to update: ")
                new_var = input("Enter new Value you want to replace with existing value: ")
                tdg.update(cursor, tableName, var, new_var, id)

                data = tdg.findAll(cursor, tableName)
                tdg.display(cursor, data, tableName)

            case 4:
                # Delete By Id
                print("Select table you want to delete data from: \n"
                      "1. bookType\n"
                      "2. book\n"
                      "3. publish\n")

                tableIndex = int(input("Enter Number: "))
                tableName = tables[tableIndex - 1]
                id = input("Enter id number: ")
                tdg.deleteById(cursor, tableName, id)

                data = tdg.findAll(cursor, tableName)
                tdg.display(cursor, data, tableName)

            case 5:
                # Exit
                print("Signing Off...")
                break
