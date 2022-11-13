from connection import Connector
import requests
import json
global url
global db
from MainGateway import TDG

params_subject = ['love', 'feminism', 'inspirational', 'authors', 'fiction', 'poetry', 'fantasy', 'romance']

class Main:
    def readApiAndInsertData(self, tdg):
        try:
            for item in params_subject:
                url = f'https://www.googleapis.com/books/v1/volumes?q={str(item)}:keyes&key=AIzaSyCB4mblXymeFZnTJKzp409fWKh8QC8Ty5Y&maxResults=5'
                api_result = requests.get(url)
                api_response = api_result.json()


                # Part 5: Simplifying Method Calls       Refactoring strategy
                self.write_data(api_response)
                data = self.read_data()
                tdg.dataInsertionIntoTable(data, item)
            return True
        except:
            return False

    def write_data(self, api_response):
        try:
            # Downloading json data into a file
            data = json.dumps(api_response)
            file = open("../api_data.json", "w")
            file.write(data)

        except:
            print("Error in File creation/ data insertion")

    def read_data(self):
        f = open("../api_data.json", "r")

        # Inline Temp Refactoring
        return json.loads(f.read())['items']

if __name__ == "__main__":
    c = Connector()
    db = c.create_connection()
    tdg = TDG()
    main = Main()

    if tdg.checkTableExists() == False:
        # Read API data into JSON
        tdg.createTables()
        var = main.readApiAndInsertData(tdg)
        if var:
            print("*************************************************\n"
                  "* Data inserted successfully into all the table *\n"
                  "*************************************************")
        else:
            print("Error in inserting Data into Databse.")
    else:
        print("Tables already exists")

    while True:
        print("*********************\n"
              "*  Select Task:     *\n"
              "*  1. FIND ALL      *\n"
              "*  2. FIND BY NAME  *\n"
              "*  3. UPDATE        *\n"
              "*  4. DELETE        *\n"
              "*  5. EXIT          *\n"
              "*********************")

        user_input = int(input("Enter Number: "))
        tables = ['bookType', 'book', 'publish']

        match user_input:
            case 1:
                # Fetch All
                print("*******************\n"
                      "*  SELECT TABLE:  *\n"
                      "*  1. bookType    *\n"
                      "*  2. book        *\n"
                      "*  3. publish     *\n"
                      "*******************\n")
                tableIndex = int(input("Enter Number: "))
                tableName = tables[tableIndex - 1]

                data = tdg.findAll(tableName)
                tdg.display(data, tableName)

            case 2:
                # Fetch By Id

                bookName = input("Enter Book Name: ")

                book_data, publish_data = tdg.findByName(bookName)
                tableName = 'book'
                tdg.display(book_data, tableName)

                tableName = 'publish'
                tdg.display(publish_data, tableName)


            case 3:
                # Update By Id
                print("SELECT TABLE: \n"
                      "1. bookType\n"
                      "2. book\n"
                      "3. publish\n")

                tableIndex = int(input("Enter Number: "))
                tableName = tables[tableIndex - 1]
                data = tdg.findAll(tableName)
                tdg.display(data, tableName)

                id = input("Enter id number: ")

                columns = tdg.getColumns(tableName)
                print(columns)
                var = input("Enter field you want to update: ")
                new_var = input("Enter new Value you want to replace with existing value: ")
                tdg.update(tableName, var, new_var, id)

                data = tdg.findAll(tableName)
                tdg.display(data, tableName)

            case 4:
                # Delete By Id

                id = input("Enter bookId you want to delete: ")
                tdg.deleteById(id)

                data = tdg.findAll('book')
                tdg.display(data, 'book')
                print("\nData deleted successfully...\n")

            case 5:
                # Exit
                print("Signing Off...")
                break
