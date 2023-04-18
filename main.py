from fastapi import FastAPI, status, APIRouter
from db import get_database, init_db
from contextlib import asynccontextmanager
import pickle
import uvicorn
import json
from fastapi.middleware.cors import CORSMiddleware
from lib import get_most_common_actor, get_most_common_movie, get_max_duration_by, get_score_count_by, get_prod_per_county

ml_model  = {}

""" @asynccontextmanager
async def lifespan(app: FastAPI):
  with open('model.pkl' , 'rb') as f:
    ml_model["answer"] = pickle.load(f)
    yield
    ml_model["answer"].clear() """

""" app = FastAPI(lifespan=lifespan) """
 
app = FastAPI()
origins = [
  "http://localhost:5000",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins='*',
  allow_methods=["GET"],
)

@app.get("/")
async def root():
  return { "running": "leonardo" }

@app.get('/api/get_max_duration')
def get_max_duration(year: int=None, platform: str=None, duration_type: str=None):
  collection = get_database()
  respuesta = get_max_duration_by(collection, year, duration_type, platform)
  print(respuesta)
  if respuesta == None:
    return {
      'pelicula': "Ups!"
    }
  return {
    'pelicula': respuesta
  }

@app.get("/api/get_score_count")
def get_score_count(platform: str, scored: int, year: int):
  collection = get_database()
  quantity = get_score_count_by(collection, platform, year, scored)

  return {
    "count": quantity
  }

@app.get("/api/get_count_platform")
def get_count_platform(platform):
  collection = get_database()
  quantity = get_most_common_movie(collection, platform)

  if not quantity:
    return {
      "data": None,
      "status": 'ok',
      "error": None
    }

  return {
    "count": quantity,
  }

@app.get('/api/get_actor')
def get_actor(platform: str, year: int):
  collection = get_database()
  obj_actor = get_most_common_actor(collection, platform, year)

  if obj_actor["_id"] == 'unknown':
    return {
    "data": None,
    "error": None,
    "status": "OK"
  }
  return {
      'actor': obj_actor["_id"],
  }

@app.get('/api/prod_per_county')
def prod_per_county(type: str, country: str, year: int):
  collection = get_database()
  count = get_prod_per_county(collection, type, country, year)

  if count == None:
    return {
      "count": None
    }

  return count

@app.get('/api/get_contents')
def get_contents(rating: str):
  collection = get_database()
  res = collection.aggregate([
    {
      "$match": {
        "rating": str(rating)
      }
    },
    {
      "$group": {
        "_id": None,
        "count": { "$sum": 1 } 
      }
    }
  ])

  quantity = {}

  for i in res:
    quantity = i

  if bool(quantity):
    return {
        'count': quantity
      }

  return {
    'count': None
  }

""" @app.get("/api/predict")
async def predict(user_id: int, title: str):
  collection = get_database()

  cursor = collection.find({
    "$and": [
      { "title": { "$eq": title }}
    ]
  })

  if cursor == None:
    return { "result": None }

  movie = {}

  for i in cursor:
    movie = i

  result = ml_model["answer"].predict(int(user_id), movie["id"]).est

  print(result)

  return { "result": result } """

"""async def main():
  config = uvicorn.Config("main:app", port=5000, log_level="info")
  server = uvicorn.Server(config)
  await server.serve()"""

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
