__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"


import sqlite3
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader


# Custom SQL agent class
class SQLAgent:
    def run(self, db_path, table_name):
        print(db_path, table_name)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        conn.close()
        return data


# Custom Website agent class
class WebsiteAgent:
    def run(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        clean_text = "\n".join(line for line in text.splitlines() if line.strip())
        return clean_text


# Custom PDF agent class
class PDFAgent:
    def run(self, pdf_files):
        text_data = []
        for pdf in pdf_files:
            reader = PdfReader(pdf)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            text_data.append(text)
        return text_data


if __name__ == '__main__':
    # obj = SQLAgent()
    # obj.run('/Users/himanshusharma/PycharmProjects/MultiAgent/TestDB/appointment_db.db', 'appointments')
    obj = WebsiteAgent()
    obj.run('https://www.greymanlab.com/')