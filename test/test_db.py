# Example Python program to insert rows into a MySQL database table

# import the mysql client for python
import pymysql

# Create a connection object
dbServerName    = "127.0.0.1"
dbUser          = "darvishan"
dbPassword      = "darvishan"
dbName          = "che_khabar"
charSet         = "utf8mb4"

connectionObject   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,
                                     db=dbName, charset=charSet)

try:
    # Create a cursor object
    cursorObject            = connectionObject.cursor()                                     

    # SQL string to create a MySQL table
    sqlCreateTableCommand   = "CREATE TABLE Employee(id int(11) AUTO_INCREMENT PRIMARY KEY, LastName varchar(32), FirstName varchar(32), DepartmentCode int)"

    # Execute the sqlQuery
    cursorObject.execute(sqlCreateTableCommand)

    # List the tables using SQL command
    sqlShowTablesCommand    = "show tables"   

    # Execute the SQL command
    cursorObject.execute(sqlShowTablesCommand)

    #Fetch all the rows - from the command output
    rows                = cursorObject.fetchall()
    for row in rows:
        print(row)

    # Insert rows into the MySQL Table
    insertStatement = "INSERT INTO Employee (id, LastName, FirstName, DepartmentCode) VALUES (1,\"Albert\",\"Einstein\",10)"   
    cursorObject.execute(insertStatement)
    
    # Get the primary key value of the last inserted row
    print("Primary key id of the last inserted row:")
    print(cursorObject.lastrowid)

    # SQL Query to retrive the rows
    sqlQuery    = "select * from Employee"   

    #Fetch all the rows - for the SQL Query
    cursorObject.execute(sqlQuery)
    rows = cursorObject.fetchall()

    for row in rows:
        print(row)

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()