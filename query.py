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
  result = collection.aggregate(query)
  platform = {}
  for i, val in enumerate(result):
    platform = val
  return platform