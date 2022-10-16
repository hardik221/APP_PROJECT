# Step 1 start by importing the code
import requests
import json
import sqlite3

try:
    #Connection with sqlite3
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")

    #Execute Drop query
    cursor.execute("drop table person2")

    #Create Table
    sqlite_select_Query = "create table person2 (sin integer PRIMARY KEY AUTOINCREMENT, name varchar(200))"
    cursor.execute(sqlite_select_Query)

    #Execute multiple queries
    operation = [(1, "Hardik"), (2, "Yash")]
    cursor.executemany("INSERT INTO person2 VALUES(?, ?)", operation)


    #Fetch data from database
    data = cursor.execute("SELECT * FROM person2").fetchall()
    print("SQLite Database Version is: ", data)
    # insert_stmt = (
    #     "INSERT INTO employees (emp_no, first_name, last_name, hire_date) "
    #     "VALUES (%s, %s, %s, %s)"
    # )
    # data = (2, 'Jane', 'Doe', datetime.date(2012, 3, 23))
    # cursor.execute(insert_stmt, data)
    #
    # select_stmt = "SELECT * FROM employees WHERE emp_no = %(emp_no)s"
    # cursor.execute(select_stmt, {'emp_no': 2})


    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)


# params = {
#     'access_key': 'dbf7c159c9b2868f6facff6675e35775'
# }
# result = requests.get('http://api.aviationstack.com/v1/flights', params)
# #result = requests.get('https://developer.nrel.gov/api/alt-fuel-stations/v1.json?fuel_type=E85,ELEC&state=CA&limit=2&api_key=QXk4ANLmbHnN47NYHufiEdbpOLd4UuESri3mZT7C')
#
# data = json.loads(result.text)
# print(data)
# columns = ['pagination','total_results','station_counts']
# for row in data:
#     keys= tuple(row[c] for c in columns)
#     cursor.execute('insert into Student values(?,?,?)',keys)
#     print(f'{row["name"]} data inserted Succefully')
#
# connection.commit()
# connection.close()

url = "https://hotels4.p.rapidapi.com/v2/get-meta-data"

headers = {
	"X-RapidAPI-Key": "45ece162f9msh277df8c13051d12p1ec734jsn3ec541518ff1",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.text)








