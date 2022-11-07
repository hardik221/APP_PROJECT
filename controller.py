import requests
import json
import pymysql
import connection

url = 'https://www.googleapis.com/books/v1/volumes?q=love:keyes&key=AIzaSyCB4mblXymeFZnTJKzp409fWKh8QC8Ty5Y&maxResults=30'


def read_api():
    global url
    api_result = requests.get(url)
    api_response = api_result.json()
    # api_data = json.dumps(api_response, indent=4)
    # new_data = json.loads(api_data)
    # for i in range(len(new_data)):
    #     print(new_data['items'][i]['id'])

    return api_response


def write_data(api_response):
    try:
        # Downloading json data into a file
        data = json.dumps(api_response)

        file = open("api_data.json", "w")
        file.write(data)
        print("API data successfully downloaded!!")
    except:
        print("Error in File creation/ data insertion")


def connect():
    # # connect to MySQL
    # #con = pymysql.connect(host = 'localhost',user = 'root',passwd = '',db = 'test')
    cursor = connection.db1.cursor()
    return cursor


def read_data():
    f = open("api_data.json", "r")
    new_data = json.loads(f.read())
    return new_data


def validate_string(val=None):
    if val != None:
        if type(val) is int:
            # for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val
    else:
        return None


def table_creation(cursor):
    drop_book = "DROP TABLE IF EXISTS Book"

    cursor.execute(drop_book)
    cursor.execute("CREATE TABLE Book "
                   "(BookId varchar(255) NOT NULL, "
                   "selfLink varchar(255),"
                   "PRIMARY KEY (BookId))")

def data_insertion_into_table(new_data):
    # parse json data to SQL insert
    for i in range(len(new_data)):
        print(new_data['items'][i]['id'], new_data['items'][i]['selfLink'])
        bookId = validate_string(new_data['items'][i]['id'])
        selfLink = validate_string(new_data['items'][i]['selfLink'])

        cursor.execute("INSERT INTO Book (BookId, selfLink) VALUES (%s, %s)", (bookId, selfLink))
    print('Data inserted successfully')
    connection.db1.commit()

if __name__ == '__main__':
    # Read API data into JSON
    json_data = read_api()

    # Create a api_data.json file and put downloaded data into that file
    write_data(json_data)

    # Connect with DB
    cursor = connect()

    # Read data from downloaded file
    data = read_data()

    # Table creation
    table_creation(cursor)

    # insert data into table
    data_insertion_into_table(data)
