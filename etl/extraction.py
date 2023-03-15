import pandas as pd

def get_dataframe(file_path):
  df = pd.read_csv(file_path)
  return df

def handle_nulls(df):
  df["director"].fillna("no", inplace=True)
  df["cast"].fillna("no", inplace=True)
  df["country"].fillna("no", inplace=True)
  #df["date_added"].fillna("no", inplace=True)
  df["rating"].fillna("G", inplace=True)
  return df

def handle_ids(df):
  df['id'] = df.apply(lambda x: "a" + x['show_id'], axis=1)
  df.drop(columns =["show_id"], inplace = True)
  return df

def handle_datefield(df):
  df["date_added"] =  pd.to_datetime(df["date_added"])
  df["date_added"] = pd.to_datetime(df["date_added"].dt.strftime('%y%m%d'))
  return df

def handle_duration(df):
  new = df["duration"].str.split(" ", n = 1, expand = True)
  df["duration_int"] = new[0]
  df["duration_int"].fillna("50", inplace=True)
  df["duration_type"] = new[1]
  df['duration_type'] = df['duration_type'].replace('Season','Seasons')
  df["duration_type"].fillna("no", inplace=True)
  df.drop(columns=["duration"], inplace = True)
  return df

def handle_lower(df):
  dtypes = df.dtypes.to_dict()
  my_type = 'object' # because str have len its not a str :| but object
  for col_name, typ in dtypes.items():
    if typ == my_type :
      df[col_name] = df[col_name].apply(str.lower)
  return df

def main(file_path):
  df = get_dataframe(file_path)
  df = handle_nulls(df)
  df = handle_ids(df)
  df = handle_datefield(df)
  df = handle_duration(df)
  #df = handle_lower(df)
  return df

if __name__ == "__main__":
  file_path1 = 'datasets/amazon_prime_titles.csv'
  file_path2 = 'datasets/disney_plus_titles.csv'
  file_path3 = 'datasets/hulu_titles.csv'
  file_path4 = 'datasets/netflix_titles.csv'
  df_1 = main(file_path3)
  #df_2 = main(file_path2)
  #df_3 = main(file_path3)
  #df_4 = main(file_path4)
  #df_t = pd.concat([df_1, df_2, df_3, df_4])
  print(df_1["duration_int"])
