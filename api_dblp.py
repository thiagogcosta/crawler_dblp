import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

local = '/home/thiago/crawler_DBLP/'

professores = ['Jó Ueyama', 'Maria da Graça Campos Pimentel', 'Rudinei Goularte', 'Renata Pontin de Mattos Fortes', 'Marcelo G. Manzato' ,'Dilvan de Abreu Moreira', 'Kamila Rios Da Hora Rodrigues']

colunas = ['autores', 'titulo', 'revista', 'volume', 'paginas', 'ano', 'doi', 'link']
df_research = pd.DataFrame(columns = colunas)

resp_profs = []
lista_artigos = []

for pf in professores:

    payload = {'q':pf, 'format':'json'}


    resp = requests.get(url='http://dblp.org/search/publ/api', params=payload)

    resp_profs.append(resp.json())

for i in range(20):
    #print(i)
    data_agora = datetime.now() + relativedelta(years = -i)

    datas = data_agora.strftime('%Y-%m-%d %H:%M:%S')

    datas = datas.split(' ')
    datas = datas[0].split('-')
    ano = datas[0]

    print('--------------------Papers no Ano de %s--------------------'%(ano))
    
    for resp in resp_profs:
    
        resp_json = resp
    
        papers = resp_json['result']['hits']['hit']
    
        for i in range(len(papers)):
            
            info = papers[i]['info']

            if(info['year'] == ano):
                
                autores = ""
                
                for j in range(len(info['authors']['author'])):

                    try:    
                        criador = info['authors']['author'][j]['text']

                        if j == 0:
                            autores = criador
                        else:
                            autores = autores + ", "+criador
                    
                    except Exception as exp:
                        print(exp)
                        pass

                titulo = None
                revista = None
                volume = None
                paginas = None
                ano = None
                doi = None
                link = None
                
                #-------------------------------Dataframe-------------------------------
                tam = len(df_research)

                df_research.loc[tam, 'autores'] = autores
                
                if "title" in info:
                    titulo = info['title']
                    df_research.loc[tam, 'titulo'] = titulo
                if "venue" in info:
                    revista = info['venue']
                    df_research.loc[tam, 'revista'] = revista
                if "volume" in info:
                    volume = info['volume']
                    df_research.loc[tam, 'volume'] = volume
                if "pages" in info:
                    paginas = info['pages']
                    df_research.loc[tam, 'paginas'] = paginas
                if "year" in info:
                    ano = info['year']
                    df_research.loc[tam, 'ano'] = ano
                if "doi" in info:
                    doi = info['doi']
                    df_research.loc[tam, 'doi'] = doi
                if "ee" in info:
                    link = info['ee']
                    df_research.loc[tam, 'link'] = link

                print(df_research)
        
        #print("---------------------------------------------------------------")

df_research.to_csv(local+ 'getDBLP.csv')
