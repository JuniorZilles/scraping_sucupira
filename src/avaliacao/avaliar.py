import json
from bs4 import BeautifulSoup
from .plot import permandent, permandentColaborador, totais, permandentApenasA


def ler_json(name: str) -> dict:
    with open(name+'.json', encoding='UTF-8') as json_file:
        data = json.load(json_file)
        return data


def avaliar():
    confer = ler_json("producoes")
    docent = ler_json("docentes")
    qualis = getQualis(confer)
    perion = getPeridicos()
    som = getSomaPeriConf(qualis, perion)
    #qualis = getQualisAno(confer)
    content = calcTotalPermananentes(qualis, docent)
    contentPer = calcTotalPermananentes(som, docent)
    contentPerA = calcTotalPermananentesA(som, docent)
    #content = calcTotalPermananentesAno(qualis, docent)
    #writeFile(content, 'sums')
    new = sorted(content.items(),key= lambda a: a[1]['totalPropPerm'])
    permandent(new, 32, "Trabalhos em Anais Ponderados Por Qualis e Por Orientador Permanente")
    new1 = sorted(content.items(), key=lambda a: a[1]['totalPermColab'])
    permandentColaborador(new1, 36, 'Trabalhos em Anais Ponderados Por Qualis e Por Orientador (Permanente + Colaborador)')
    new2 = sorted(content.items(), key=lambda a: a[1]['proporcao'])
    totais(new2, 38, 'Trabalhos em Anais Ponderados Por Qualis')

    new = sorted(contentPer.items(),key= lambda a: a[1]['totalPropPerm'])
    permandent(new,27, "Trabalhos em Anais + Periódicos Ponderados Por Qualis e Por Orientador Permanente")
    new1 = sorted(contentPer.items(), key=lambda a: a[1]['totalPermColab'])
    permandentColaborador(new1,36, 'Trabalhos em Anais + Periódicos Ponderados Por Qualis e Por Orientador (Permanente + Colaborador)')
    new = sorted(contentPerA.items(),key= lambda a: a[1]['totalPropPerm'])
    permandentApenasA(new,22, "Trabalhos em Anais + Periódicos Ponderados Por Qualis A e Por Orientador Permanente")
    new2 = sorted(contentPer.items(), key=lambda a: a[1]['proporcao'])
    totais(new2,36, 'Trabalhos em Anais + Periódicos Ponderados Por Qualis')
    

def getSomaPeriConf(conf:dict, perio:dict) -> dict:
    content= {}
    for c in conf.keys():
        if c in conf and c in perio:
            content[c] = {}
            for b in conf[c].keys():
                content[c][b] = conf[c][b] + int(perio[c][b])
    return content

def getPeridicos() -> dict:
    file = open("periodicos/contagem_qualis.html", "r")
    content = file.read()
    file.close()
    soup = BeautifulSoup(content, features="lxml")
    trs = soup.find_all("tr")
    content = {}
    for tr in trs:
        td = tr.find_all('td')
        progr = td[1].get_text()
        a1 = td[2].get_text()
        a2 = td[3].get_text()
        a3 = td[4].get_text()
        a4 = td[5].get_text()
        b1 = td[6].get_text()
        b2 = td[7].get_text()
        b3 = td[8].get_text()
        b4 = td[9].get_text()
        c = td[10].get_text()
        nf = td[11].get_text()
        total = td[12].get_text()
        # if progr == "UFSCAR-CC-3" or progr == "UFSCAR-CC-4":
        #     progr = "UFSCAR-CC-3-4"
        if progr not in content:
            content[progr] = {"A1": a1, "A2": a2, "A3": a3, "A4": a4, "B1": b1,
                              "B2": b2, "B3": b3, "B4": b4, "C": c, "NF": nf, "total": total}
        else:
            content[progr]['A1'] += a1
            content[progr]['A2'] += a2
            content[progr]['A3'] += a3
            content[progr]['A4'] += a4
            content[progr]['B1'] += b1
            content[progr]['B2'] += b2
            content[progr]['B3'] += b3
            content[progr]['B4'] += b4
            content[progr]['C'] += c
            content[progr]['NF'] += nf
            content[progr]['total'] += total
    return content


def getQualis(confer: dict) -> dict:
    content = {}
    for c in confer.keys():
        total = 0
        for x in confer[c]:
            if c not in content:
                content[c] = {"A1": 0, "A2": 0, "A3": 0, "A4": 0, "B1": 0,
                              "B2": 0, "B3": 0, "B4": 0, "C": 0, "NF": 0, "total": 0}
            content[c][x['qualis']] += 1
            total += 1
        content[c]['total'] = total
    return content

def getQualisAno(confer: dict) -> dict:
    content = {}
    for c in confer.keys():
        total = 0
        for x in confer[c]:
            if c not in content:
                content[c] = {"2017":{"A1": 0, "A2": 0, "A3": 0, "A4": 0, "B1": 0,
                              "B2": 0, "B3": 0, "B4": 0, "C": 0, "NF": 0}, 
                              "2018":{"A1": 0, "A2": 0, "A3": 0, "A4": 0, "B1": 0,
                              "B2": 0, "B3": 0, "B4": 0, "C": 0, "NF": 0},
                              "2019":{"A1": 0, "A2": 0, "A3": 0, "A4": 0, "B1": 0,
                              "B2": 0, "B3": 0, "B4": 0, "C": 0, "NF": 0}}
            content[c][x['ano']][x['qualis']] += 1
            total += 1
        content[c].update({'total': total})
    return content


def calcTotalPermananentes(qualis: dict, docentes: dict):
    for c in qualis.keys():
        pc = (docentes[c]['permanente']+docentes[c]['colaborador'])/3
        p = (docentes[c]['permanente'])/3
    
        qA1 = qualis[c]['A1'] * 1
        qA2 = qualis[c]['A2']*0.875
        qA3 = qualis[c]['A3']*0.75
        qA4 = qualis[c]['A4']*0.625
        qB1 = qualis[c]['B1']*0.5
        qB2 = qualis[c]['B2']*0.2
        qB3 = qualis[c]['B3']*0.1
        qB4 = qualis[c]['B4']*0.05
        qC = qualis[c]['C']*0
        qNF = qualis[c]['NF']*0
        total = qA1 + qA2 + qA3 + qA4 + qB1 + qB2 + qB3 + qB4 + qC + qNF
        totalP = total/p
        totalPc = total/pc
        qualis[c].update({
            "qA1": qA1, "qA2": qA2, "qA3": qA3, "qA4": qA4, "qB1": qB1, "qB2": qB2, "qB3": qB3, "qB4": qB4, "qC": qC, "qNF": qNF, "proporcao": total, "totalPropPerm": totalP,
            "totalPermColab": totalPc, "permCola": pc, "perm": p})
    return qualis

def calcTotalPermananentesA(qualis: dict, docentes: dict):
    for c in qualis.keys():
        p = (docentes[c]['permanente'])/3
    
        qA1 = qualis[c]['A1'] * 1
        qA2 = qualis[c]['A2']*0.875
        qA3 = qualis[c]['A3']*0.75
        qA4 = qualis[c]['A4']*0.625
    
        total = qA1 + qA2 + qA3 + qA4
        totalP = total/p
        qualis[c].update({
            "qA1": qA1, "qA2": qA2, "qA3": qA3, "qA4": qA4, "proporcao": total, "totalPropPerm": totalP,
             "perm": p})
    return qualis

def calcTotalPermananentesAno(qualis: dict, docentes: dict):
    for c in qualis.keys():
        for k in ['2017', '2018', '2019']:
            qA1 = qualis[c][k]['A1'] * 1
            qA2 = qualis[c][k]['A2']*0.875
            qA3 = qualis[c][k]['A3']*0.75
            qA4 = qualis[c][k]['A4']*0.625
            qB1 = qualis[c][k]['B1']*0.5
            qB2 = qualis[c][k]['B2']*0.2
            qB3 = qualis[c][k]['B3']*0.1
            qB4 = qualis[c][k]['B4']*0.05
            qC = qualis[c][k]['C']*0
            qNF = qualis[c][k]['NF']*0
            total = qA1 + qA2 + qA3 + qA4 + qB1 + qB2 + qB3 + qB4 + qC + qNF
            qualis[c][k].update({
                "qA1": qA1, "qA2": qA2, "qA3": qA3, "qA4": qA4, "qB1": qB1, "qB2": qB2, "qB3": qB3, "qB4": qB4, "qC": qC, "qNF": qNF, "total":total})
    return qualis

def writeFile(data: dict, name: str):
    a_file = open(name+".json", "w", encoding="UTF-8")
    json.dump(data, a_file)
    a_file.close()
