from fastapi import FastAPI, status, APIRouter
import asyncio
import uvicorn
from db import get_database
import routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes.router, tags=['Movies'], prefix='/api/movies')

# AÑO, PLATAFORMA Y TIPO DE DURACIÓN
#/?first=1&second=12&third=5
@app.get('/api/get_max_duration')
def get_max_duration(year: int, platform: str, duration_type: str):
  query = {
    "$and": [
      { "release_year": { "$eq": int(year) }},
      { "duration_type": { "$eq": duration_type }},
      # { "id": { "$regex" : "^a"} }
      { "platform": { "$eq": platform }}
    ]
  }

  collection = get_database()
  q = collection.find(query)
  for item in q:
    print(item)

  return {
    "error": None,
    "status": "Ok"
  }

""" Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año (la función debe llamarse get_score_count(platform, scored, year))
[] platform $eq
[] scored > XX
[] year $eq
"""

@app.get("/api/get_score_count")
def get_score_count(platform: str, score: int, year: int):
  first_letter = platform[:1]
  print(platform, score, year, first_letter)
  print(platform, float(score), int(year), first_letter)

  collection = get_database()
  result = collection.aggregate([
    { "$match": { "release_year": 2015, "platform": "amazon" } },
    {
      "$lookup": {
        "from": "ratings",
        "localField": "id",
        "foreignField": "movieId",
        "as": "ratings_docs",
      }
    }
    #{
    #  "$group": {
    #    "_id": None,
    #    "count": { "$sum": 1 }
    #  }
    #}
  ])
  print("[FINE]")

  print("RESULT:", list(result))
  for item in result:
    print(item)
  
  return {
    "error": None,
    "status": "Ok"
  }

""" Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))
 """
@app.get("/api/get_count_platform")
def get_count_platform(platform):
  collection = get_database()
  query = [
    {
      "$match": {
        "platform": platform
      }
    },
    {
      "$group": {
        "_id": "$platform",
        "count": {
          "$sum": 1
        }
      }
    }
  ]
  result = collection.aggregate(query)
  actor = {}
  if not result:
    return {
      "data": None,
      "status": 'ok',
      "error": None
    }

  for i, val in enumerate(result):
    actor = val

  return {
    "data": actor,
    "status": 'ok',
    "error": None
  }
  
""" Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year)) """

@app.get('/api/get_actor')
def get_actor(platform: str, year: int):
  collection = get_database()
  query = [
    {
      "$match": {"platform": platform, "release_year": int(year) }
    },
    { "$group" : {"_id":"$director", "count":{"$sum":1}} },
    { 
      "$sort": { "count": -1 } 
    },
    {
      "$limit": 2
    }
  ]
  result = collection.aggregate(query)

  res = []
  for item in result:
    res.append(item)
  actor = res[-1]["_id"]

  #Check null values
  if actor == 'no':
    return {
    "data": { "actor": None },
    "error": None,
    "status": "OK"
  }

  count = res[-1]["count"]
  return {
    "data": {"actor": actor, "count": count },
    "error": None,
    "status": "OK"
  }