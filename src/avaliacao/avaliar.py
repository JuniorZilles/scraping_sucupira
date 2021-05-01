import json
from .plot import permandent, permandentColaborador, totais
def ler_json(name:str)->dict:
    with open(name+'.json', encoding='UTF-8') as json_file:
        data = json.load(json_file)
        return data

def avaliar():
    confer = ler_json("producoes")
    docent = ler_json("docentes")
    qualis = getQualis(confer)
    content = calcTotalPermananentes(qualis,docent )
    # writeFile(content, 'sums')
    # new = sorted(content.items(),key= lambda a: a[1]['totalPropPerm'])
    # permandent(new)
    # new1 = sorted(content.items(), key=lambda a: a[1]['totalPermColab'])
    # permandentColaborador(new1)
    new2 = sorted(content.items(), key=lambda a: a[1]['total'])
    totais(new2)

def getQualis(confer:dict) ->dict:
    content = {}
    for c in confer.keys():
        total = 0
        for x in confer[c]:
            if c not in content:
                content[c] = {"A1": 0,"A2":0,"A3":0,"A4":0,"B1":0,"B2":0,"B3":0,"B4":0,"C":0,"NF":0, "total":0 }
            content[c][x['qualis']] += 1
            total += 1
        content[c]['total'] = total
    return content

def calcTotalPermananentes(qualis:dict, docentes:dict):
    for c in qualis.keys():
        pc = (docentes[c]['permanente']+docentes[c]['colaborador'])/3
        p = (docentes[c]['permanente'])/3
        total = qualis[c]['A1'] * 1 + qualis[c]['A2']*0.875 + qualis[c]['A3']*0.75 + qualis[c]['A4']*0.625 + qualis[c]['B1']*0.5 + qualis[c]['B2']*0.2 + qualis[c]['B3']*0.1 + qualis[c]['B4']*0.05 + qualis[c]['C']*0 + qualis[c]['NF']*0
        totalP = total/p
        totalPc = total/pc
        qualis[c].update({"proporcao":total, "totalPropPerm": totalP, "totalPermColab":totalPc, "permCola":pc, "perm":p})
    return qualis

def writeFile(data:dict, name:str):
    a_file = open(name+".json", "w", encoding="UTF-8")
    json.dump(data, a_file)
    a_file.close()