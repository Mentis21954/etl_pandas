import pandas as pd
from extract import extract_info_from_artist, extract_titles_from_artist, extract_listeners_from_titles_by_artist, find_info_for_titles
from transform import clean_the_text, merge_titles_data, remove_wrong_values, drop_duplicates_titles, integrate_data
from load import load_to_database

# find names from csv file
df = pd.read_csv('spotify_artist_data.csv')
artist_names = list(df['Artist Name'].unique())

# find info and return a dataframe
artist_contents = extract_info_from_artist(artist_names[:2])
# clean the text info from dataframe
content_df = clean_the_text(artist_contents)

for name in artist_names[:2]:
  releases = extract_titles_from_artist(name)
  listeners = extract_listeners_from_titles_by_artist(name, releases)
  releases_info = find_info_for_titles(releases)

  releases_df = merge_titles_data(releases_info, listeners)
  releases_df = remove_wrong_values(releases_df)
  releases_df = drop_duplicates_titles(releases_df)

  data = integrate_data(content_df, releases_df, name)
  load_to_database(data)   