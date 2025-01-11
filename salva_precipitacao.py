#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 23:58:23 2025

@author: marina
"""

#%% imports

import re
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np
import sqlite3
#%% organizar datas
test_date = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y%m%d'), "%Y%m%d")
date_generated = pd.date_range(test_date, periods=10)
datas = date_generated.strftime("%Y%m%d").to_list()

gdrv_file = '/home/marina/projetos/para-precipitacao/precip.db'

#%% Recuperar conteúdo da página
main_url = 'https://www.foreca.com/103439062/Katuet%C3%A9-La-Paloma-Paraguay/10-day-forecast'
html_doc = requests.get(main_url).text

soup = BeautifulSoup(html_doc, 'html.parser')

valores = []
for span in soup.find_all('span','value rain rain_mm')[:-1]:
  if span.text[0] == '<':
    valor = 0.05
  else:
    valor = float(re.findall(r"[-+]?(?:\d*\.*\d+)",span.text)[0])
  valores.append(valor)
  
lt_conn = sqlite3.connect(gdrv_file)
db_cursor = lt_conn.cursor()

cidade = "Katueté"

for i in np.arange(len(datas)):
  query = f"""
  Insert into previsoes(cidade, data_real, data_previsao, valor_previsao)
  values ('{cidade}',{datas[0]},{datas[i]},{valores[i]}) """

  db_cursor.execute(query)
  lt_conn.commit()

db_cursor.close()
lt_conn.close()





#%%
# import sqlite3
# lt_conn = sqlite3.connect(gdrv_file)
# db_cursor = lt_conn.cursor()
# db_cursor.execute("select * from previsoes")
# db_rows = db_cursor.fetchall()
# print(db_rows[0])
# db_cursor.close()
# lt_conn.close()