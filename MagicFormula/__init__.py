# TODO: implement Magic Formula python code from link below
# https://medium.com/@b.marquiori/is-joel-greenblatts-magic-formula-really-magic-2ef13db30296

import pandas as pd
import numpy as np
import requests as rq

url = 'http://www.fundamentus.com.br/resultado.php'


header = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"  
 }
r = rq.get(url, headers=header)


df = pd.read_html(r.text,  decimal=',', thousands='.')[0]


for column in ['Div.Yield', 'Mrg Ebit', 'Mrg. Líq.', 'ROIC', 'ROE', 'Cresc. Rec.5a']:
  df[column] = df[column].str.replace('.', '')
  df[column] = df[column].str.replace(',', '.')
  df[column] = df[column].str.rstrip('%').astype('float') / 100
  
ranking = pd.DataFrame()
ranking['pos'] = range(1,151)
ranking['EV/EBIT'] = df[ df['EV/EBIT'] > 0 ].sort_values(by=['EV/EBIT'])['Papel'][:150].values
ranking['ROIC'] = df.sort_values(by=['ROIC'], ascending=False)['Papel'][:150].values

ranking = pd.concat([
    ranking.pivot_table(columns='EV/EBIT', values='pos'),
    ranking.pivot_table(columns='ROIC', values='pos')
])

ranking = ranking.dropna(axis=1).sum()


n_shares = 15
magicformula = ranking.sort_values()[:n_shares]
magicformula = magicformula.to_frame(name = "MF_ranking")

print(magicformula)