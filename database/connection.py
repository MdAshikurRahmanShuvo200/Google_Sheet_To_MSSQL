import pyodbc
from config import *


def get_connection():

    connection_string = f"""
    DRIVER={{ODBC Driver 17 for SQL Server}};
    SERVER={DB_SERVER};
    DATABASE={DB_DATABASE};
    UID={DB_USERNAME};
    PWD={DB_PASSWORD};
    TrustServerCertificate=yes;
    """

    return pyodbc.connect(connection_string)