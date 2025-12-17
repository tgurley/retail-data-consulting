import pandas as pd
import mysql.connector

# Load CSV
df = pd.read_csv("data/online_retail.csv")

# Basic Cleaning
df = df.dropna(subset=["CustomerID"])
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user=input("Enter username: "),
    password=input("Enter password: ")
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS retail_db")
cursor.execute("USE retail_db")

cursor.execute("""
CREATE TABLE IF NOT EXISTS retail_sales (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description TEXT,
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DECIMAL(10,2),
    CustomerID INT,
    Country VARCHAR(50),
    Revenue DECIMAL(10,2)
)               
""")

insert_sql = """
INSERT INTO retail_sales
(InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country, Revenue)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

data = [
    (
        row.InvoiceNo,
        row.StockCode,
        row.Description,
        int(row.Quantity),
        row.InvoiceDate,
        float(row.UnitPrice),
        int(row.CustomerID),
        row.Country,
        float(row.Revenue)
    )
    for _, row in df.iterrows()
]

cursor.executemany(insert_sql, data)
conn.commit()
cursor.close()

print("Data loaded successfully.")