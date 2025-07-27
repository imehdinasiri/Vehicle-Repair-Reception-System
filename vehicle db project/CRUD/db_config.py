import pyodbc

def get_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=MEHDI;'
        'DATABASE=CarRepairDB;'
        'Trusted_Connection=yes;'
    )
    return conn
