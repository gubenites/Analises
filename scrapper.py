import requests
from bs4 import BeautifulSoup
import pprint as pp
import pandas as pd
import unidecode

def get_g1_text(topic):
    URL = 'https://g1.globo.com/{}/'.format(topic)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    titles = soup.find_all('a', {'class' : 'feed-post-link gui-color-primary gui-color-hover'})
    descs = soup.find_all('div', {'class' : 'feed-post-body-resumo'})

    noticias = []
    counter = 0

    for title, desc in zip(titles, descs):
        if counter < 5:
            noticias.append({
                'title' : unidecode.unidecode(title.text), 
                'desc' : unidecode.unidecode(desc.text),
                'link' : title['href']
                }
            )
        counter += 1

    return pd.DataFrame(noticias)

title1 = 'economia/agronegocios'
df1 = get_g1_text(title1)
df1['Title'] = title1

title2 = 'ciencia/'
df2 = get_g1_text(title2)
df2['Title'] = title2

frames = [df1,df2]
df3 = pd.concat(frames)

pp.pprint(df3.head())

df3.to_csv('out.csv')




