import os

from dotenv import load_dotenv

load_dotenv()

USER = 'root'
PASSWORD = 'admin'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'main'

print(USER, PASSWORD, HOST, PORT, DATABASE)
