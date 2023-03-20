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
  
#mongodb+srv://printer:<password>@clustercu.yfxun.mongodb.net/?retryWrites=true&w=majority
#DATABASE_URL = os.getenv("DATABASE_URL")

def get_database():
  client = init_db()
  db = client["cu"]
  collection = db["movies_clean"]
  return collection
    

  #try:
  #  db_cu = db.cu
    #yield db_cu
  #finally:
  #  db_cu.close()