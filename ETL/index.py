import pandas as pd
from constants import dicc
import numpy as np

def get_dataframe(file_path):
  df = pd.read_csv(file_path)
  return df

def get_df_rating(file_path):
  df = pd.read_csv(file_path)
  return df

def handle_nulls(df):
  df["director"].fillna("unknown", inplace=True)
  df["cast"].fillna("unknown", inplace=True)
  df["country"].fillna("unknown", inplace=True)
  #df["date_added"].fillna("no", inplace=True)
  df["rating"].fillna("G", inplace=True)
  # remove if contain min | seasons or season in col
  df = df[~df['rating'].str.contains('min')]
  df = df[~df['rating'].str.contains('seasons')]
  df = df[~df['rating'].str.contains('season')]
  return df

def handle_ids(df, id, platform):
  df['id'] = df.apply(lambda x: id + x['show_id'], axis=1)
  df.drop(columns =["show_id"], inplace = True)
  df["platform"] = platform
  return df

def handle_datefield(df):
  df["date_added"] =  pd.to_datetime(df["date_added"])
  df["date_added"] = pd.to_datetime(df["date_added"].dt.strftime('%y%m%d'))
  return df

def handle_duration(df):
  new = df["duration"].str.split(" ", n = 1, expand = True)
  df["duration_int"] = new[0]
  #df["duration_int"] = new[0].astype(np.int16)
  df["duration_int"] = df["duration_int"].apply(lambda x: int(x) if type(x) == np.dtype('U') else x)
  mean = df["duration_int"].mean(axis=0, numeric_only=True, skipna=True)
  df["duration_int"].fillna(round(mean), inplace=True)
  df["duration_type"] = new[1]
  df['duration_type'] = df['duration_type'].replace('Season','Seasons')
  df["duration_type"].fillna("unknown", inplace=True)
  df.drop(columns=["duration"], inplace = True)
  return df

def handle_lower(df):
  # convert to lowerCase only strings in pands should be object thing
  dtypes = df.dtypes.to_dict()
  my_type = 'object' # because str have len its not a str :| but object
  for col_name, typ in dtypes.items():
    if typ == my_type:
      df[col_name] = df[col_name].str.lower()
  return df

def get_mean_score(movie_id, mean_ss):
  m_s = mean_ss[movie_id]
  return m_s

def create_score_mean_col(df, df_rating):
  mean_ss = df_rating.groupby("movieId")["rating"].mean()
  df["mean_score"] = df["id"].apply(lambda x: get_mean_score(x, mean_ss))
  return df


def main(file_path, id, platform, df_rating):
  df = get_dataframe(file_path)
  print("_----------------->>>", platform)
  print(df.isna().sum())
  df = handle_nulls(df)
  df = handle_ids(df, id, platform)
  df = handle_datefield(df)
  df = handle_duration(df)
  df = handle_lower(df)
  df = create_score_mean_col(df, df_rating)
  print(df.head(3))
  print("***********[END]**********")
  return df

if __name__ == "__main__":
  clean_dfs = []
  df_rating = get_df_rating('out_ratings.csv')

  for i, val in enumerate(dicc):
    clean_df = main(val["file_path"], val["id"], val["platform"], df_rating)
    clean_dfs.append(clean_df)

  merged_df = pd.concat(clean_dfs)
  print(merged_df.shape)
  compression_opts = dict(method='zip',
                        archive_name='movies_clean.csv')

  merged_df.to_csv('movies_clean.zip', encoding='utf-8', index=False, compression=compression_opts) 

