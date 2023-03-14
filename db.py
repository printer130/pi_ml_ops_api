from pymongo import MongoClient
from dotenv import load_dotenv
import os
# from os.path import join, dirname
# dotenv_path = join(dirname(__file__), '.env')
load_dotenv()
DATABASE_NAME = os.environ.get("DATABASE_NAME")

def get_database():
  db = MongoClient(DATABASE_NAME)
  db_cu = db.cu
  return db_cu
  #try:
  #  db_cu = db.cu
    #yield db_cu
  #finally:
  #  db_cu.close()