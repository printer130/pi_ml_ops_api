import pandas as pd
from constants import dicc
import numpy as np

def get_dataframe(file_path):
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

def main(file_path, id, platform):
  df = get_dataframe(file_path)
  print("_----------------->>>", platform)
  print(df.isna().sum())
  df = handle_nulls(df)
  df = handle_ids(df, id, platform)
  df = handle_datefield(df)
  df = handle_duration(df)
  df = handle_lower(df)
  return df

if __name__ == "__main__":
  clean_dfs = []

  for i, val in enumerate(dicc):
    clean_df = main(val["file_path"], val["id"], val["platform"])
    clean_dfs.append(clean_df)

  merged_df = pd.concat(clean_dfs)
  print(merged_df.shape)
  compression_opts = dict(method='zip',
                        archive_name='out.csv')

  merged_df.to_csv('out.zip', encoding='utf-8', index=False, compression=compression_opts) 

