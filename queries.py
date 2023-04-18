def score_count_query(platform, year, scored):
  query = [
    {
      "$match": { 
        "type": "movie",
        "platform": platform,
        "release_year": int(year),
        "mean_score": { "$gte": scored }
      }
    },
    { "$count": "quantity" }
  ]
  return query

def max_duration_by(platform, year, duration_type):
  filters = []

  if year:
    filters.append({ "release_year": { "$eq": int(year) }})
  if platform:
    filters.append({ "platform": { "$eq": platform }})
  if duration_type:
    filters.append({ "duration_type": { "$eq": duration_type }})

  query = { "$and": filters }
  return query

def most_common_actor(platform, year):
  query = [
    {
      "$match": {"platform": platform, "release_year": int(year), "type": "movie" }
    },
    { "$group" : {"_id":"$director", "count":{"$sum":1}} },
    { 
      "$sort": { "count": -1 } 
    },
    {
      "$limit": 2
    }
  ]
  return query

def most_common_movie(platform):
  query = [
    {
      "$match": {
        "platform": platform,
        "type": "movie"
      }
    },
    {
      "$group": {
        "_id": "$platform",
        "count": {
          "$sum": 1
        }
      }
    },
    {
      "$project": {
        "_id": 0,
        "count": 1
      }
    }
  ]
  return query