from pymongo import MongoClient
from dotenv import load_dotenv
import os
# from os.path import join, dirname
# dotenv_path = join(dirname(__file__), '.env')
load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_database():
  client = MongoClient(DATABASE_URL)
  db = client["cu"]
  collection = db["with_types"]
  return collection
  #try:
  #  db_cu = db.cu
    #yield db_cu
  #finally:
  #  db_cu.close()