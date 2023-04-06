import pandas as pd
import time
import requests
from constants import LASTFM_API_KEY, DISCOGS_API_KEY


def extract_info_from_all_artists(artists_names):
    artist_contents = {}

    # extract for all artists' informations from last fm and store as a dict
    for name in artists_names:
        url = ('https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=') + name + (
            '&api_key=') + LASTFM_API_KEY + ('&format=json')
        artist_info = requests.get(url).json()
        artist_contents.update({name: artist_info['artist']['bio']['content']})
        print('Search infrmation for artist {} ...'.format(name))

    # return artist info as a dataframe for transform stage
    return pd.DataFrame(artist_contents.values(), columns=['Content'], index=artist_contents.keys())


def extract_titles_from_artist(name):
    # get the artist id from artist name
    url = ('https://api.discogs.com/database/search?q=') + name + ('&{?type=artist}&token=') + DISCOGS_API_KEY
    discogs_artist_info = requests.get(url).json()
    id = discogs_artist_info['results'][0]['id']

    print('Search releases from discogs.com for artist {} ...'.format(str(name)))

    # with id get artist's releases
    url = ('https://api.discogs.com/artists/') + str(id) + ('/releases')
    releases = requests.get(url).json()
    releases_df = pd.json_normalize(releases['releases'])

    # store the tracks info in a list
    tracks_info = []
    for index, url in enumerate(releases_df['resource_url'].values):
        source = requests.get(url).json()
        # search if exists track's price
        if 'lowest_price' in source.keys():
            # print(str(index) + ': '+ str(source['title'])+ ' '+ str(source['lowest_price']))
            if 'formats' in source.keys():
                tracks_info.append((source['title'], releases_df['artist'].iloc[index], source['year'],
                                    source['formats'][0]['name'], source['lowest_price']))
            else:
                tracks_info.append(
                    (source['title'], releases_df['artist'].iloc[index], source['year'], None, source['lowest_price']))
            print('Found ' + str((index + 1)) + ' titles!')

        # sleep 3 secs to don't miss requests
        time.sleep(3)

    print('Find tracks from artist ' + name + ' with Discogs ID: ' + str(id))

    # return artist's tracks as a dataframe for transform stage
    return pd.DataFrame(tracks_info, columns=['Title', 'Collaborations', 'Year', 'Format', 'Discogs Price'])
