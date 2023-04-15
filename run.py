import pandas as pd
from extract import extract_info_from_artist, extract_titles_from_artist
from transform import remove_wrong_values, drop_duplicates_titles, clean_the_text, integrate_data
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
    releases_df = remove_wrong_values(releases)
    releases_df = drop_duplicates_titles(releases_df)

    data = integrate_data(content_df, releases_df, name)
    load_to_database(data)
