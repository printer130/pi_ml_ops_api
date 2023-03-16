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
@app.get('/api')
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
