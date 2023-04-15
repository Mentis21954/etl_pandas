import pandas as pd

def clean_the_text(content: dict):
    content_df = pd.DataFrame(content.values(), columns=['Content'], index=content.keys())
    
     # remove new line commands, html tags and "", ''
    content_df['Content'] = content_df['Content'].replace(r'\r+|\n+|\t+', '', regex=True)
    content_df['Content'] = content_df['Content'].replace(r'<[^<>]*>', '', regex=True)
    content_df['Content'] = content_df['Content'].replace(r'"', '', regex=True)
    content_df['Content'] = content_df['Content'].replace(r"'", '', regex=True)
    print('Clean the informations text')

    return content_df


def remove_wrong_values(releases: dict):
    df = pd.DataFrame(releases)

    # find and remove the rows/titles where there are no selling prices in discogs.com
    df = df[df['Discogs Price'].notna()]
    print('Remove releases where have wrong year value in discogs.com')
    # keep only the rows has positive value of year
    df = df[df['Year'] > 0]
    print('Remove releases where there no selling price in discogs.com')
    
    return df


def drop_duplicates_titles(df):
    df = df.drop_duplicates(subset=['Title'])
    print('Find and remove the duplicates titles if exist!')
    return pd.DataFrame(
        data={'Collaborations': df['Collaborations'].values, 'Year': df['Year'].values, 'Format': df['Format'].values,
              'Discogs Price': df['Discogs Price'].values}, index=(df['Title'].values))


def integrate_data(content_df, releases_df, name):
    return {'Artist': name,
            'Description': content_df['Content'][name],
            'Releases': releases_df.to_dict('index')
            }