__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"

import pandas as pd
import sqlite3


def push_csv_to_sqlite(csv_path, db_path, table_name):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()


if __name__ == '__main__':
    csv_path = '/Users/himanshusharma/PycharmProjects/MultiAgent/TestDB/Appointment Scheduling Cleaned Data.csv'
    db_path = '/Users/himanshusharma/PycharmProjects/MultiAgent/TestDB/appointment_db.db'
    table_name = 'appointments'
    push_csv_to_sqlite(csv_path, db_path, table_name)
