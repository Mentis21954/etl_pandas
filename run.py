import pandas as pd
from extract import extract_info_from_artist, extract_titles_from_artist, extract_playcounts_from_titles_by_artist, find_info_for_titles
from transform import clean_the_text, remove_wrong_values, merge_titles_data, drop_duplicates_titles, integrate_data
from load import load_to_database

# find names from csv file
df = pd.read_csv('spotify_artist_data.csv')
artist_names = list(df['Artist Name'].unique())

# find info and return a dataframe
artist_contents = extract_info_from_artist(artist_names[:2])
# clean the text info from dataframe
content_df = clean_the_text(artist_contents)

for name in artist_names[:2]:
  # extract
  releases = extract_titles_from_artist(name)
  playcounts = extract_playcounts_from_titles_by_artist(name, releases)
  releases = find_info_for_titles(releases)
  # transform
  releases = remove_wrong_values(releases)
  releases_df = merge_titles_data(releases, playcounts)
  releases_df = drop_duplicates_titles(releases_df)
  data = integrate_data(content_df, releases_df, name)
  # load
  load_to_database(data)   