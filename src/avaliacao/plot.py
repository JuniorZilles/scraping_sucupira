import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def permandent(indices: list):
    data = []
    pesosB = [0, 0.5, 0.2, 0.1, 0.05]
    pesosA = [0, 1, 0.875, 0.75, 0.625]
    for x in indices:
        d = []
        d.append(x[0])
        prop = x[1]['proporcao']
        totalprop = x[1]['totalPropPerm']
        d.append(0)
        d.append(0)
        for j in range(4, 0, -1):
            k = ((x[1]['B'+str(j)]*pesosB[j]) * totalprop) / prop
            d.append(k)
        for j in range(4, 0, -1):
            k = ((x[1]['A'+str(j)]*pesosA[j]) * totalprop) / prop
            d.append(k)
        print(d)
        data.append(d)
        # create data
    df = pd.DataFrame(data,
                      columns=['Programas', 'NA', 'C', 'B4', 'B3', 'B2', 'B1', 'A4', 'A3', 'A2', 'A1'])
    df.sort_values('Programas')
    df.plot(x='Programas', kind='bar', stacked=True,
            title='Trabalhos em Anais Ponderados Por Qualis e Por Orientador Permanente',)
    plt.grid(True)
    plt.savefig('grafico_perm.png', dpi=1920, orientation='portrait')
    plt.show()


def permandentColaborador(indices: list):
    data = []
    pesosB = [0, 0.5, 0.2, 0.1, 0.05]
    pesosA = [0, 1, 0.875, 0.75, 0.625]
    for x in indices:
        d = []
        d.append(x[0])
        prop = x[1]['proporcao']
        totalprop = x[1]['totalPermColab']
        d.append(0)
        d.append(0)
        for j in range(4, 0, -1):
            k = ((x[1]['B'+str(j)]*pesosB[j]) * totalprop) / prop
            d.append(k)
        for j in range(4, 0, -1):
            k = ((x[1]['A'+str(j)]*pesosA[j]) * totalprop) / prop
            d.append(k)
        print(d)
        data.append(d)
    df = pd.DataFrame(data,
                      columns=['Programas', 'NA', 'C', 'B4', 'B3', 'B2', 'B1', 'A4', 'A3', 'A2', 'A1'])
    df.sort_values('Programas')
    df.plot(x='Programas', kind='bar', stacked=True,
            title='Trabalhos em Anais Ponderados Por Qualis e Por Orientador (Permanente + Colaborador)')
    plt.grid(True)
    plt.savefig('grafico_perm_col.png', dpi=1920, orientation='portrait')
    plt.show()


def totais(indices: list):
    data = []
    for x in indices:
        d = []
        d.append(x[0])
        d.append(x[1]['NF'])
        d.append(x[1]['C'])
        for j in range(4, 0, -1):
            d.append(x[1]['B'+str(j)])
        for j in range(4, 0, -1):
            d.append(x[1]['A'+str(j)])
        print(d)
        data.append(d)
    df = pd.DataFrame(data,
                      columns=['Programas', 'NA', 'C', 'B4', 'B3', 'B2', 'B1', 'A4', 'A3', 'A2', 'A1'])
    df.plot(x='Programas', kind='bar', stacked=True,
            title='Trabalhos em Anais Ponderados Por Qualis')
    plt.grid(True)
    plt.savefig('grafico_totais.png', dpi=1920, orientation='portrait')
    plt.show()