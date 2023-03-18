from fastapi import FastAPI, status, APIRouter
from db import get_database, init_db

import uvicorn
import json
#from fastapi.middleware.cors import CORSMiddleware
from query import get_most_common_actor, get_most_common_movie, get_max_duration_by

app = FastAPI()

origins = [
    "http://localhost:8000",
]

""" app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) """

@app.on_event("shutdown")
async def app_shutdown():
    await init_db().close()

@app.get("/")
async def root():
    return { "running": "leonardo" }

""" Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. (la función debe llamarse get_max_duration(year, platform, duration_type)) """
@app.get('/api/get_max_duration')
def get_max_duration(year: int=None,platform: str=None, duration_type: str=None):
  print(year,platform,duration_type)
  collection = get_database()
  movies_json = get_max_duration_by(collection, year, duration_type, platform)
  if movies_json == None:
    return {
      "data": None
    }
  return {
    "data": movies_json,
    "error": None,
    "status": "Ok"
  }

""" Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año (la función debe llamarse get_score_count(platform, scored, year))
"""
@app.get("/api/get_score_count")
def get_score_count(platform: str, score: int, year: int):
  first_letter = platform[:1]

  collection = get_database()
  cursor = collection.aggregate([
    {
      "$match": {
        "release_year": 2015,
        "platform": "amazon"
      }
    },
    {
      "$lookup": {
        "from": "ratings",
        "localField": "id",
        "foreignField": "movieId",
        "as": "rating_table"
      }
    },
    {
      "$unwind": "$rating_table"
    },
    {
      "$match": {
        "rating_table.rating": { "$gte": 4 }
      }
    },
    {
      "$group": { "_id": None, "count": {"$sum": 1}}
    }
  ])

  #l = []
  for item in cursor:
    print(item)
  #  l.append(item)
  #count = len(l)
  #print(count)
  
  return {
    "error": None,
    "status": "Ok"
  }

""" Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))
 """
@app.get("/api/get_count_platform")
def get_count_platform(platform):
  collection = get_database()
  movie = get_most_common_movie(collection, platform)

  if not movie:
    return {
      "data": None,
      "status": 'ok',
      "error": None
    }

  return {
    "data": movie,
    "status": 'ok',
    "error": None
  }
  
""" Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year)) """

@app.get('/api/get_actor')
def get_actor(platform: str, year: int):
  collection = get_database()
  obj_actor = get_most_common_actor(collection, platform, year)

  actor = obj_actor["_id"]
  count = obj_actor["count"]
  #Check null values or if exists
  if actor == 'no':
    return {
    "data": None,
    "error": None,
    "status": "OK"
  }
  
  return {
    "data": {"actor": actor, "count": count },
    "error": None,
    "status": "OK"
  }

""" def fake_answer_to_everything_ml_model(x: float):
    return x * 42 """

ml_models = {}

""" @asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()
app = FastAPI(lifespan=lifespan) """

@app.get("/api/predict")
async def predict(x: float):
  result = ml_models["answer_to_everything"](x)
  return {"result": result} 


""" async def main():
  config = uvicorn.Config("main:app", port=5000, log_level="info")
  server = uvicorn.Server(config)
  await server.serve() """

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
