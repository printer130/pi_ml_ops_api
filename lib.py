import json
from datetime import datetime
from typing import Any
from queries import score_count_query, max_duration_by, most_common_actor, most_common_movie
from bson import ObjectId

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

def get_max_duration_by(collection, year, duration_type, platform):
  result = {}
  query = max_duration_by(platform, year, duration_type)
  cursor = collection.find(query).sort("duration_int", -1).limit(1)
  for i in cursor:
    result = i
  if result["title"] == None:
    return None
  return result["title"]

def get_score_count_by(collection, platform, year, scored):
  result = {}
  query = score_count_query(platform, year, scored)
  cursor = collection.aggregate(query)
  for i in cursor:
    result = i

  if len(result) == 0:
    return 0
  
  return result["quantity"]

def get_most_common_actor(collection, platform, year):
  res = []
  query = most_common_actor(platform, year)
  result = collection.aggregate(query)
  for item in result:
    res.append(item)

  # return last actor after counting null values
  obj_actor = res[-1]

  return obj_actor

def get_most_common_movie(collection, platform):
  result = {}
  query = most_common_movie(platform)
  cursor = collection.aggregate(query)
  for i in cursor:
    result = i

  if result["count"] == None:
    return None

  return result["count"]

def get_prod_per_county(collection, type, country, year):
  result = {}
  res = collection.aggregate([
    {
      "$match": {"type": type, "release_year": int(year), "country": country }
    },
    { 
      "$group": {
         "_id": None,
         "count": { "$sum": 1 } 
      }
    }
  ])
  for i in res:
    result["count"] = i["count"]
    
  return result
