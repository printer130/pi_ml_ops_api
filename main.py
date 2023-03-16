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
def get_score_count(platform: str, scored: int, year: int):
  first_letter = platform[:1]
  print(platform, scored, year, first_letter)
  collection = get_database()
  result = collection.aggregate([
    {
      "$lookup": {
        "from": "ratings",
        "let": { 
          "platform_id_item": platform,
          "release_year_item": year
        },
        "pipeline": [
            { "$match":
              { "$expr":
                  { "$and":
                    [
                      { "$eq": [ "$movieId",  "$$platform_id_item" ] },
                      { "$eq": [ "$movieId",  "$$release_year_item" ] },
                      #{ "$gte": [ "$", "$$release_year_item" ] }
                    ]
                  }
              }
            },
          # { $project: { stock_item: 0, _id: 0 } }
        ],
        "as": "stockmovies"
      }
    }
  ])
  for item in result:
    print(item)
  
  return {
    "error": None,
    "status": "Ok"
  }