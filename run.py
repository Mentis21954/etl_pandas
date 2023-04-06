import pandas as pd
from extract import extract_titles_from_artist, extract_info_from_all_artists
from transform import remove_null_prices, drop_duplicates_titles, clean_the_text, integrate_data
from load import load_to_database

# find names from csv file
df = pd.read_csv('spotify_artist_data.csv')
artist_names = list(df['Artist Name'].unique())

# find info and return a dataframe
content_df = extract_info_from_all_artists(artist_names[:2])
# clean the text info from dataframe
content_df = clean_the_text(content_df)

for name in artist_names[:2]:
    releases_df = extract_titles_from_artist(name)
    releases_df = remove_null_prices(releases_df)
    releases_df = drop_duplicates_titles(releases_df)

    data = integrate_data(content_df, releases_df, name)
    load_to_database(data)
