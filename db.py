from pymongo import MongoClient
from dotenv import load_dotenv

import os

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
def init_db():
  try:
    client = MongoClient(DATABASE_URL)
    return client
  finally:
    client.close()
  
def get_database(doc = "movies"):
  client = init_db()
  db = client["plat"]
  collection = db[doc]
  return collection

  #try:
  #  db_cu = db.cu
    #yield db_cu
  #finally:
  #  db_cu.close()