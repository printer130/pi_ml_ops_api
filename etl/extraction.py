import pandas as pd
from constants import dicc

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

def handle_ids(df, id):
  df['id'] = df.apply(lambda x: id + x['show_id'], axis=1)
  df.drop(columns =["show_id"], inplace = True)
  return df

def handle_datefield(df):
  df["date_added"] =  pd.to_datetime(df["date_added"])
  df["date_added"] = pd.to_datetime(df["date_added"].dt.strftime('%y%m%d'))
  return df

def handle_duration(df):
  new = df["duration"].str.split(" ", n = 1, expand = True)
  #df["duration_int"] = new[0]
  df["duration_int"] = new[0].astype('Int64')
  mean = df["duration_int"].mean(axis=0, numeric_only=True, skipna=True)
  df["duration_int"].fillna(int(mean), inplace=True)
  df["duration_type"] = new[1]
  df['duration_type'] = df['duration_type'].replace('Season','Seasons')
  df["duration_type"].fillna("no", inplace=True)
  df.drop(columns=["duration"], inplace = True)
  return df

def handle_lower(df):
  dtypes = df.dtypes.to_dict()
  print(df.dtypes)
  my_type = 'object' # because str have len its not a str :| but object
  for col_name, typ in dtypes.items():
    if typ == my_type:
      df[col_name] = df[col_name].str.lower()
  return df

def main(file_path, id):
  df = get_dataframe(file_path)
  df = handle_nulls(df)
  df = handle_ids(df, id)
  df = handle_datefield(df)
  df = handle_duration(df)
  df = handle_lower(df)
  return df

if __name__ == "__main__":
  clean_dfs = []

  for i, val in enumerate(dicc):
    clean_df = main(val["file_path"], val["id"])
    clean_dfs.append(clean_df)

  merged_df = pd.concat(clean_dfs)
  print(merged_df.shape)
  compression_opts = dict(method='zip',
                        archive_name='out.csv')
  merged_df.to_csv('out.zip', encoding='utf-8', index=False, compression=compression_opts) 

