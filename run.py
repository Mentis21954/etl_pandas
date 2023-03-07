from extract import extract_artist_names, extract_titles_from_artist, extract_info_from_all_artists
from transform import remove_null_prices, drop_duplicates_titles, convert_df_to_dict, clean_the_text
from load import load_to_dabase

# find names from csv file
artist_names = extract_artist_names()

# find info and return a dataframe
artist_contents_df = extract_info_from_all_artists(artist_names[:2])
# clean the text info from dataframe
artist_contents_df = clean_the_text(artist_contents_df)

print(artist_contents_df)
# print(artist_contents_df['Content'][0])

for name in artist_names[:1]:
    tracks_df = extract_titles_from_artist(name)
    tracks_df = remove_null_prices(tracks_df)
    tracks_df = drop_duplicates_titles(tracks_df)
    tracks = convert_df_to_dict(tracks_df, name)
    if name in artist_contents_df.index:
        tracks.update({'Description': artist_contents_df['Content'][name]})
        load_to_dabase(tracks)
        print('Artist {} insert to DataBase!'.format(name))
