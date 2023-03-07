import pandas as pd
import time
import requests


def extract_artist_names():
    df = pd.read_csv('spotify_artist_data.csv')
    # return artist names
    return list(df['Artist Name'].unique())


def extract_info_from_all_artists(artists_names):
  artist_contents = {}

  # extract for all artists' informations from last fm and store as a dict
  for name in artists_names:
    url = ('https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=')+name+('&api_key=')+LASTFM_API_KEY+('&format=json')
    artist_info = requests.get(url).json()
    artist_contents.update({name: artist_info['artist']['bio']['content']})

  df = pd.DataFrame(artist_contents.items(), columns= ['Artist','Content'])
  print(df.head())
  return  clean_the_text(df)


def extract_titles_from_artist(name):
  url = ('https://api.discogs.com/database/search?q=')+name+('&{?type=artist}&token=')+ DISCOGS_API_KEY
  discogs_artist_info = requests.get(url).json()
  id = discogs_artist_info['results'][0]['id']

  print('Search titles from artist '+ name+ '...')

  url = ('https://api.discogs.com/artists/') + str(id) + ('/releases')
  releases = requests.get(url).json()
  releases_df = pd.json_normalize(releases['releases'])

  tracks_info = []
  for index,url in enumerate(releases_df['resource_url'].values):
    source = requests.get(url).json()
    if 'lowest_price' in source.keys():
        #print(str(index) + ': '+ str(source['title'])+ ' '+ str(source['lowest_price']))
        if 'formats' in source.keys():
          tracks_info.append((source['title'], releases_df['artist'].iloc[index], source['year'], source['formats'][0]['name'], source['lowest_price']))
        else:
          tracks_info.append((source['title'], releases_df['artist'].iloc[index], source['year'], None, source['lowest_price']))
        print('Found '+ str((index+1))+' titles!')

    # sleep 3 secs to don't miss requests
    time.sleep(3)

  print('Find songs from artist '+ name + ' with id: '+ str(id))
  # return artist's titles as a dataframe for transform stage
  df = pd.DataFrame(tracks_info, columns= ['Title', 'Collaborations', 'Year','Format','Discogs Price'])
  print(df.head())
  return remove_null_prices(df,name)