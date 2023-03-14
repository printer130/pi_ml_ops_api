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

@app.get('/')
def get_name():
  return { 'hola': 'hello leonardo' }

@app.get('/{year}/{platform}/{duration_type}')
def get_max_duration():
  return 'get_max_duration'

@app.get('/{movieId}')
def get_max_duration():
  #movies = get_database.amazon_prime_titles.find()
  return "movies"
# year, platform, duration_type