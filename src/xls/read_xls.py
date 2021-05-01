import os
import pandas as pd
import re
import json
from src.data.postgres import PostgresClient 
from .map import mappingto, mappingfrom

def getPath(pasta):
    lista = []
    for nome in os.listdir(pasta):
        lista.append({"caminho": os.path.join(pasta, nome), "nome":nome.replace('.xls', "")})
    return lista

def read_producoes():
    folder = 'producoes'
    paths = getPath(folder)
    listaConteudo = {}
    
    for path in paths:
        df = pd.read_csv(path['caminho'], sep='\t', encoding='LATIN-1')
        df.columns = list(range(18))
        name = buildName(path['nome'])
        if name not in listaConteudo:
            listaConteudo[name] = []
        for row in df.index:
            titulo = df[5][row]
            subtipo = df[11][row]
            detalhamento = df[12][row]
            evento = df[13][row]
            if detalhamento == "Nome do evento" and subtipo == "TRABALHO EM ANAIS":
                qualis, eventoCerto = getQualis(evento)
                listaConteudo[name].append({'inst': buildName(path['nome']), 'titulo':titulo, 'eventoCorreto':eventoCerto, 'eventoOriginal':evento, 'qualis':qualis})
    writeFile(listaConteudo, folder)

def read_docentes():
    folder = 'docentes'
    paths = getPath(folder)
    listaConteudo = {}
    for path in paths:
        df = pd.read_csv(path['caminho'], sep='\t', encoding='LATIN-1')
        df.columns = list(range(18))
        name, periodo = buildNamePeriodo(path['nome'])
        if name not in listaConteudo:
            listaConteudo[name] = {periodo:{"permanente":0, "colaborador":0}}
        for row in df.index:
            categoria = df[13][row]
            if categoria == "PERMANENTE":
                listaConteudo[name][periodo]['permanente'] += 1
            elif categoria == "COLABORADOR":
                listaConteudo[name][periodo]['colaborador'] += 1
    writeFile(listaConteudo, folder)

def writeFile(data:dict, name:str):
    a_file = open(name+".json", "w", encoding="UTF-8")
    json.dump(data, a_file)
    a_file.close()

def buildName(value:str):
    first = value.find('-')
    last = value.rfind('-')
    return value[first+1:last]

def buildNamePeriodo(value:str) -> tuple:
    first = value.find('-')
    last = value.rfind('-')

    return value[first+1:last], value[:first]

def getQualis(evento:str) -> tuple:
    client = PostgresClient()
    evento = evento.replace('\r\n', '')
    efirst = evento.find('(')
    elast = evento.rfind(')')
    rqualis = 'NF'
    revento = 'NF'
    for a in range(0,len(mappingfrom)):
        if mappingfrom[a] in evento:
            evento = evento.replace(mappingfrom[a], mappingto[a])
    row = None
    # caso a sigla seja o evento
    row = client.one_row_connection_db(getEqualitySiglaQuery(), (evento,))
    # caso a sigla esteja entre parenteses
    if row == None:
        if efirst != -1 and elast != -1:
            sigla = evento[efirst+1:elast].upper().replace(' ', '').replace('-', '')
            sigla = re.sub('[0-9]', '', sigla)
            row = client.one_row_connection_db(getEqualitySiglaQuery(), (sigla,))
            if row == None:
                search = evento[:efirst]
                row = client.one_row_connection_db(getSimilarityQuery(), (search,search,))      
    spl = evento.split('-')
    if len(spl) == 0:
        spl = evento.split(' ')
    if row == None and len(spl) > 0:
        for a in spl:
            b = a.strip().split(' ')
            for c in b:
                row = client.one_row_connection_db(getEqualitySiglaQuery(), (c,))
                if row != None:
                    break
            if row != None:
                break
    if row == None:
        tempevento = re.sub('[0-9]', '', evento)
        tempevento = tempevento.replace('"', '').replace("'", "").replace("-", "").replace(",", "").replace(".", "")
        row = client.one_row_connection_db(getSimilarityQuery(), (tempevento,tempevento,))
    if row == None:
        spl = evento.split(',')
        for a in spl:
            row = client.one_row_connection_db(getSimilarityQuery(), (a,a,))
            if row != None:
                break
    if row == None:
        spl = evento.split('-')
        for a in spl:
            row = client.one_row_connection_db(getSimilarityQuery(), (a,a,))
            if row != None:
                break
    
    if row != None:
        if len(row) > 0:
            revento = row[0]
            rqualis = row[1]
    client.close()
    return rqualis, revento

def getSimilarityQuery():
    return "SELECT conferencia, qualis, ginfo.similarity(ginfo.retira_acentuacao(lower(conferencia)), ginfo.retira_acentuacao(lower((%s)))) as similaridade FROM ginfo.qualis WHERE ginfo.similarity(ginfo.retira_acentuacao(lower(conferencia)), ginfo.retira_acentuacao(lower((%s)))) > 0.6 ORDER BY similaridade DESC LIMIT 1;"

def getEqualitySiglaQuery():
    return "SELECT conferencia, qualis FROM ginfo.qualis WHERE lower(sigla) = lower(%s);"

def getEqualitySiglaInQuery():
    return "SELECT conferencia, qualis FROM ginfo.qualis WHERE lower(sigla) IN %s;"