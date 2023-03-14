from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from db import get_database

router = APIRouter()

@router.get("/{id}", response_description="Get a single movie by id")
def get_movies(id: str, request: Request):
    if (movie := get_database().collection().find_one({"_id": id})) is not None:
        return movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")