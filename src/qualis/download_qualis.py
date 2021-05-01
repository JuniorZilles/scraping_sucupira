import requests
from bs4 import BeautifulSoup
from .model_qualis import QualisModel
from src.data.postgres import PostgresClient

def start():
    from src.data.init_db import DatabaseHandler
    db_handler = DatabaseHandler()
    db_created = True
    if not db_handler.exist_db():
        print('Início criação do banco')
        db_created = db_handler.create_db()
        if db_created:
            print('Banco criado') 
        else: 
            raise Exception('Banco não foi criado')

def import_qualis():
    start()
    r = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vTZsntDnttAWGHA8NZRvdvK5A_FgOAQ_tPMzP7UUf-CHwF_3PHMj_TImyXN2Q_Tmcqm2MqVknpHPoT2/pubhtml?gid=0&single=true') 
    convertToObject(r.text)

def convertToObject(html:str):
    client = PostgresClient()
    soup = BeautifulSoup(html, features="lxml")
    table = soup.find("table", {"class": "waffle"})
    tbody = table.find("tbody")
    trs = tbody.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        sigla = tds[0].get_text()
        conferencia = tds[1].get_text()
        qualis = tds[6].get_text()
        if(sigla != '' and conferencia != '' and qualis != '' and sigla != 'sigla'):
            client.no_result_connection_db("INSERT INTO ginfo.qualis (sigla, conferencia, qualis) VALUES (%s, %s, %s)", (sigla, conferencia, qualis,))
            
