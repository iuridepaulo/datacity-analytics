import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

def conectar():
    cliente = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'), serverSelectionTimeoutMS=5000)
    try:
        cliente.admin.command('ping')
        return cliente, cliente['datacity_db']
    except PyMongoError:
        cliente.close()
        raise
