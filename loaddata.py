import pyodbc
from connect_db import connect_db


def loadRentalPlan(filename, conn):
    """
        Input:
            $filename: "RentalPlan.txt"
            $conn: you can get it by calling connect_db()
        Functionality:
            1. Create a table named "RentalPlan" in the "VideoStore" database on Azure
            2. Read data from "RentalPlan.txt" and insert them into "RentalPlan"
               * Columns are separated by '|'
               * You can use executemany() to insert multiple rows in bulk
    """
    # WRITE YOUR CODE HERE
    conn.execute("create table RentalPlan(pid INT, pname VARCHAR(50), monthly_fee FLOAT, "
                 "max_movies INT, primary key(pid))")
    insert = "insert into RentalPlan(pid, pname, monthly_fee, max_movies) values(?,?,?,?)"
    file = open(filename, 'r')
    data = []
    for i in file:
        row = i.strip().split('|')
        data.append(row)
    conn.cursor().executemany(insert, data)
    file.close()


def loadCustomer(filename, conn):
    """
        Input:
            $filename: "Customer.txt"
            $conn: you can get it by calling connect_db()
        Functionality:
            1. Create a table named "Customer" in the "VideoStore" database on Azure
            2. Read data from "Customer.txt" and insert them into "Customer".
               * Columns are separated by '|'
               * You can use executemany() to insert multiple rows in bulk
    """
    # WRITE YOUR CODE HERE
    conn.execute("create table Customer(cid INT, pid INT, username VARCHAR(50), password VARCHAR(50), "
                 "primary key(cid), foreign key(pid) references RentalPlan(pid) on delete cascade)")
    insert = "insert into Customer(cid, pid, username, password) values(?,?,?,?)"
    file = open(filename, 'r')
    data = []
    for i in file:
        row = i.strip().split('|')
        data.append(row)
    conn.cursor().executemany(insert, data)
    file.close()


def loadMovie(filename, conn):
    """
        Input:
            $filename: "Movie.txt"
            $conn: you can get it by calling connect_db()
        Functionality:
            1. Create a table named "Movie" in the "VideoStore" database on Azure
            2. Read data from "Movie.txt" and insert them into "Movie".
               * Columns are separated by '|'
               * You can use executemany() to insert multiple rows in bulk
    """
    # WRITE YOUR CODE HERE
    conn.execute("create table Movie(mid INT, mname VARCHAR(50), year INT, primary key(mid))")
    insert = "insert into Movie(mid, mname, year) values(?,?,?)"
    file = open(filename, 'r')
    data = []
    for i in file:
        row = i.strip().split('|')
        data.append(row)
    conn.cursor().executemany(insert, data)
    file.close()


def loadRental(filename, conn):
    """
        Input:
            $filename: "Rental.txt"
            $conn: you can get it by calling connect_db()
        Functionality:
            1. Create a table named "Rental" in the VideoStore database on Azure
            2. Read data from "Rental.txt" and insert them into "Rental".
               * Columns are separated by '|'
               * You can use executemany() to insert multiple rows in bulk
    """
    # WRITE YOUR CODE HERE
    conn.execute("create table Rental(cid INT, mid INT, date_and_time DATETIME, status VARCHAR(6),foreign key(cid) "
                 "references Customer(cid), foreign key(mid) references Movie(mid) on delete cascade)")
    insert = "insert into Rental(cid, mid, date_and_time, status) values(?,?,?,?)"
    file = open(filename, 'r')
    data = []
    for i in file:
        row = i.strip().split('|')
        data.append(row)
    conn.cursor().executemany(insert, data)
    file.close()


def dropTables(conn):
    conn.execute("DROP TABLE IF EXISTS Rental")
    conn.execute("DROP TABLE IF EXISTS Customer")
    conn.execute("DROP TABLE IF EXISTS RentalPlan")
    conn.execute("DROP TABLE IF EXISTS Movie")


if __name__ == "__main__":
    conn = connect_db()

    dropTables(conn)

    loadRentalPlan("RentalPlan.txt", conn)
    loadCustomer("Customer.txt", conn)
    loadMovie("Movie.txt", conn)
    loadRental("Rental.txt", conn)

    conn.commit()
    conn.close()
