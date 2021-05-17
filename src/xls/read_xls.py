import os
import pandas as pd
import re
import json
from src.data.postgres import PostgresClient 
from .map import mappingfrom
from .map_to import mappingto

def getPath(pasta):
    lista = []
    for nome in os.listdir(pasta):
        if 'UFSCAR' in nome:
            lista.append({"caminho": os.path.join(pasta, nome), "nome":nome.replace('.xls', "")})
    return lista

def read_producoes():
    folder = 'producoes'
    paths = getPath(folder)
    listaConteudo = {}
    
    for path in paths:
        df = pd.read_csv(path['caminho'], sep='\t', encoding='LATIN-1')
        df.columns = list(range(18))
        periodo = "0"
        name, periodotemp = buildNamePeriodo(path['nome'])
        if (periodotemp == "699"): periodo = "2019"
        elif (periodotemp == "579"): periodo = "2018"
        elif (periodotemp == "439"): periodo = "2017"
        if name not in listaConteudo:
            listaConteudo[name] = []
        for row in df.index:
            titulo = df[5][row]
            subtipo = df[11][row]
            detalhamento = df[12][row]
            evento = df[13][row]
            if detalhamento == "Nome do evento" and subtipo == "TRABALHO EM ANAIS":
                qualis, eventoCerto = getQualis(evento)
                listaConteudo[name].append({'inst': name, 'titulo':titulo, 'eventoCorreto':eventoCerto, 'eventoOriginal':evento, 'qualis':qualis, "ano": periodo})
    writeFile(listaConteudo, folder)

def read_docentes():
    folder = 'docentes'
    paths = getPath(folder)
    listaConteudo = {}
    for path in paths:
        name, periodo = buildNamePeriodo(path['nome'])
        df = pd.read_csv(path['caminho'], sep='\t', encoding='LATIN-1')
        df.columns = list(range(18))
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
    nome = value[first+1:last]
    notaid = value[last+1:]
    if "UFSCAR" in nome:
        nota = "4" if notaid == "928" else "3"
        return nome+"-"+nota, value[:first]
    return nome, value[:first]

def getQualis(evento:str) -> tuple:
    client = PostgresClient()
    evento = evento.replace('\r\n', '').strip()
    match = re.search(r'\(\w+\)', evento)

    #efirst = evento.find('(')
    #elast = evento[efirst:].find(')')
    #elast = evento.rfind(')')
    rqualis = 'NF'
    revento = 'NF'
    consulta = ''
    for a in range(0,len(mappingfrom)):
        if mappingfrom[a].lower() in evento.lower():
            evento = evento.lower().replace(mappingfrom[a].lower(), mappingto[a])
    row = None

    consulta = evento
    # caso a sigla seja o evento
    sigla = re.sub('[0-9]', '', evento).strip()
    if('LARS/SBR' in sigla):
        print(sigla)
    row = client.one_row_connection_db(getEqualitySiglaQuery(), (sigla,))
    if row == None:
        row = client.one_row_connection_db(getEqualityConferencia(), (evento,))
    # caso a sigla esteja entre parenteses
    if row == None:
        if match != None: #if efirst != -1 and elast != -1:
            #sigla = evento[efirst+1:efirst+elast].upper().replace(' ', '').replace('-', '')
            sigla = match.group().replace('(', "").replace(')', "").replace('-', '')
            sigla = re.sub('[0-9]', '', sigla).strip()
            row = client.one_row_connection_db(getEqualitySiglaQuery(), (sigla,))
            consulta = sigla
            if row == None:
                efirst = evento.find(sigla) - 1
                search = evento[:efirst]
                row = client.one_row_connection_db(getSimilarityQuery(), (search,search,))   
                consulta = search   
    
    if row == None:
        tempevento = re.sub('[0-9]', '', evento)
        tempevento = re.sub(r'\(\w+\)','', tempevento)
        tempevento = tempevento.replace('"', '').replace("'", "").replace("-", "").replace(",", "").replace(".", "").strip()
        row = client.one_row_connection_db(getSimilarityQuery(), (tempevento,tempevento,))
        consulta = tempevento
    if row == None:
        spl = evento.split(',')
        for a in spl:
            row = client.one_row_connection_db(getSimilarityQuery(), (a.strip(),a.strip(),))
            consulta = a.strip()
            if row != None:
                break
    spl = evento.split('-')
    if row == None and len(spl) > 0:
        for a in spl:
            row = client.one_row_connection_db(getEqualitySiglaQuery(), (a.strip(),))
            consulta = a.strip()
            if row != None:
                break
    if row == None and len(spl) > 0:
        for a in spl:
            tempevento = re.sub('[0-9]', '', a)
            tempevento = re.sub(r'\(\w+\)','', tempevento)
            tempevento = tempevento.replace('"', '').replace("'", "").replace("-", "").replace(",", "").replace(".", "").strip()
            row = client.one_row_connection_db(getSimilarityQuery(), (tempevento,tempevento,))
            consulta = a.strip()
            if row != None:
                break
   
    
    
    if row != None:
        if len(row) > 0:
            revento = row[0]
            rqualis = row[1]
            #if (revento == "Latin American Symposium on Theoretical Informatics"):
            print(f'{consulta} - {revento}')
    client.close()
    return rqualis, revento

def getSimilarityQuery():
    return "SELECT conferencia, qualis, ginfo.similarity(ginfo.retira_acentuacao(lower(conferencia)), ginfo.retira_acentuacao(lower((%s)))) as similaridade FROM ginfo.qualis WHERE ginfo.similarity(ginfo.retira_acentuacao(lower(conferencia)), ginfo.retira_acentuacao(lower((%s)))) > 0.7 ORDER BY similaridade DESC LIMIT 1;"

def getEqualitySiglaQuery():
    return "SELECT conferencia, qualis FROM ginfo.qualis WHERE lower(sigla) = lower(%s);"

def getEqualitySiglaInQuery():
    return "SELECT conferencia, qualis FROM ginfo.qualis WHERE lower(sigla) IN %s;"

def getEqualityConferencia():
    return "SELECT conferencia, qualis FROM ginfo.qualis WHERE lower(conferencia) = lower(%s);"