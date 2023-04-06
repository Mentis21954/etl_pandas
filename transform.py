import pandas as pd


def remove_null_prices(df):
    # find and remove the rows/titles where there are no selling prices in discogs.com
    df = df[df['Discogs Price'].notna()]
    # print(df.head())
    print('Remove tracks where there no selling price in discogs.com')
    return df


def drop_duplicates_titles(df):
    df = df.drop_duplicates(subset=['Title'])
    print('Find and remove the duplicates titles if exist!')
    return pd.DataFrame(
        data={'Collaborations': df['Collaborations'].values, 'Year': df['Year'].values, 'Format': df['Format'].values,
              'Discogs Price': df['Discogs Price'].values}, index=(df['Title'].values))


def convert_df_to_dict(df, name):
    dict = {}
    dict.update({'Artist': name})
    # split dataframe by index
    dict.update({'Releases': df.to_dict('index')})

    return dict

def integrate_data(content_df, releases_df, name):
    return {'Artist': name,
            'Description': content_df['Content'][name],
            'Releases': releases_df.to_dict('index')
            }



def clean_the_text(contents_df):
    # remove new line command and html tags
    contents_df['Content'] = contents_df['Content'].replace('\n', '', regex=True)
    contents_df['Content'] = contents_df['Content'].replace(r'<[^<>]*>', '', regex=True)
    print('Clean the informations text')

    return contents_df
