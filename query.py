import json
from datetime import datetime
from typing import Any

from bson import ObjectId

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

def get_max_duration_by(collection, year, duration_type, platform):
  filters = []
  if year:
    filters.append({ "release_year": { "$eq": int(year) }})
  if platform:
    filters.append({ "platform": { "$eq": platform }})
  if duration_type:
    filters.append({ "duration_type": { "$eq": duration_type }})

  query = { "$and": filters }

  cursor = collection.find(query).sort("duration_int", -1).limit(1)
  data_json = MongoJSONEncoder().encode(list(cursor))
  return data_json

def get_score_count_by(collection, platform, year, score):
  cursor = collection.aggregate([
    {
      "$match": { "platform": platform, "release_year": int(year), "mean_score": { "$gte": score }}
    },
    { "$count": "quantity" }
  ])
  count_score = MongoJSONEncoder().encode(list(cursor))
  return count_score

def get_most_common_actor(collection,platform,year):
  res = []
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
  for item in result:
    res.append(item)

  # return last actor after counting null values
  obj_actor = res[-1]

  return obj_actor

def get_most_common_movie(collection, platform):
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
  cursor = collection.aggregate(query)
  result = MongoJSONEncoder().encode(list(cursor))
  return result
