import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd


def permandent(indices: list, posicao:int, titulo:str):
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
    ax = df.plot.bar(x='Programas', stacked=True,
            title=titulo)
    ax.add_patch(Rectangle(xy= ax.containers[0][posicao].get_xy(), 
                         width=ax.containers[0][posicao].get_width(),
                        height=ax.containers[0][posicao].get_height() 
                              +ax.containers[1][posicao].get_height()
                              +ax.containers[2][posicao].get_height()
                              +ax.containers[3][posicao].get_height()
                              +ax.containers[4][posicao].get_height()
                              +ax.containers[5][posicao].get_height()
                              +ax.containers[6][posicao].get_height()
                              +ax.containers[7][posicao].get_height()
                              +ax.containers[8][posicao].get_height()
                              +ax.containers[9][posicao].get_height(), 
                       fc='none', ec='red', linewidth=2))
    plt.grid(True)
    plt.savefig('grafico_perm.png', dpi=1920, orientation='portrait')
    plt.show()


def permandentApenasA(indices: list, posicao:int, titulo:str):
    data = []
    pesosA = [0, 1, 0.875, 0.75, 0.625]
    for x in indices:
        d = []
        d.append(x[0])
        prop = x[1]['proporcao']
        totalprop = x[1]['totalPropPerm']
        for j in range(4, 0, -1):
            k = ((x[1]['A'+str(j)]*pesosA[j]) * totalprop) / prop
            d.append(k)
        print(d)
        data.append(d)
        # create data
    df = pd.DataFrame(data,
                      columns=['Programas', 'A4', 'A3', 'A2', 'A1'])
    ax = df.plot.bar(x='Programas', stacked=True,
            title=titulo)
    ax.add_patch(Rectangle(xy= ax.containers[0][posicao].get_xy(), 
                         width=ax.containers[0][posicao].get_width(),
                        height=ax.containers[0][posicao].get_height() 
                              +ax.containers[1][posicao].get_height()
                              +ax.containers[2][posicao].get_height()
                              +ax.containers[3][posicao].get_height()
                              , 
                       fc='none', ec='red', linewidth=2))
    plt.grid(True)
    plt.savefig('grafico_perm.png', dpi=1920, orientation='portrait')
    plt.show()


def permandentColaborador(indices: list, posicao:int, titulo:str):
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
    ax = df.plot.bar(x='Programas', stacked=True,
            title=titulo)
    ax.add_patch(Rectangle(xy= ax.containers[0][posicao].get_xy(), 
                         width=ax.containers[0][posicao].get_width(),
                        height=ax.containers[0][posicao].get_height() 
                              +ax.containers[1][posicao].get_height()
                              +ax.containers[2][posicao].get_height()
                              +ax.containers[3][posicao].get_height()
                              +ax.containers[4][posicao].get_height()
                              +ax.containers[5][posicao].get_height()
                              +ax.containers[6][posicao].get_height()
                              +ax.containers[7][posicao].get_height()
                              +ax.containers[8][posicao].get_height()
                              +ax.containers[9][posicao].get_height(), 
                       fc='none', ec='red', linewidth=2))
    plt.grid(True)
    plt.savefig('grafico_perm_col.png', dpi=1920, orientation='portrait')
    plt.show()


def totais(indices: list, posicao:int, titulo:str):
    data = []
    for x in indices:
        d = []
        d.append(x[0])
        d.append(x[1]['qNF'])
        d.append(x[1]['qC'])
        for j in range(4, 0, -1):
            d.append(x[1]['qB'+str(j)])
        for j in range(4, 0, -1):
            d.append(x[1]['qA'+str(j)])
        print(d)
        data.append(d)
    df = pd.DataFrame(data,
                      columns=['Programas', 'NA', 'C', 'B4', 'B3', 'B2', 'B1', 'A4', 'A3', 'A2', 'A1'])

    ax = df.plot.bar(x='Programas', stacked=True,
            title=titulo)
    ax.add_patch(Rectangle(xy= ax.containers[0][posicao].get_xy(), 
                         width=ax.containers[0][posicao].get_width(),
                        height=ax.containers[0][posicao].get_height() 
                              +ax.containers[1][posicao].get_height()
                              +ax.containers[2][posicao].get_height()
                              +ax.containers[3][posicao].get_height()
                              +ax.containers[4][posicao].get_height()
                              +ax.containers[5][posicao].get_height()
                              +ax.containers[6][posicao].get_height()
                              +ax.containers[7][posicao].get_height()
                              +ax.containers[8][posicao].get_height()
                              +ax.containers[9][posicao].get_height(), 
                       fc='none', ec='red', linewidth=2))
    plt.grid(True)
    plt.savefig('grafico_totais.png', dpi=1920, orientation='portrait')
    plt.show()