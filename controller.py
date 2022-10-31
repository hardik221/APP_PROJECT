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
    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)



url = "https://movies-app1.p.rapidapi.com/api/movies"

headers = {
	"X-RapidAPI-Key": "45ece162f9msh277df8c13051d12p1ec734jsn3ec541518ff1",
	"X-RapidAPI-Host": "movies-app1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.text)

