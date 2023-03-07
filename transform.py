import pandas as pd

def remove_null_prices(df, name):
  # find and remove the rows/titles where there are no selling prices from discogs.com
  df = df[df['Discogs Price'].notna()]
  #print(df.head())

  return convert_df_to_dict(df, name)


def convert_df_to_dict(df, name):
  dict = {}
  dict.update({'Artist': name})
  dict.update({'Releases': df.to_dict('index')})

  return dict


def clean_the_text(contents_df):
  # remove new line command and html tags
  contents_df['Content'] = contents_df['Content'].replace('\n','', regex=True)
  contents_df['Content'] = contents_df['Content'].replace(r'<[^<>]*>', '', regex=True)
  #contents_df['Content'][0]

  return contents_df