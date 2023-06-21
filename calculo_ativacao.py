import os
import math
import json
import argparse 
from utils import util
import pandas as pd
from prettytable import PrettyTable


# Definição de argumentos
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--name')
parser.add_argument('-r', '--roll', dest='roll', default=None)
parser.add_argument('-m', '--minimo_ativacao', dest='minimo_ativacao', type=int)

arguments = parser.parse_args()

# Definição de constantes
amostra         = 10000
header_tabela   = ['Valor', '% Queda']

temp_dir = 'temp/ativacao'

def gerar_dataset(roll, name):
    dataset = []

    for _ in range(amostra):
        dataset.append(util.roll(roll))

    return dataset 

def montar_retorno(dataset, minimo_ativacao):
    dataset = dataset

    dataset = pd.Series(dataset).astype(int)
    dataset = (dataset.value_counts(normalize=True).mul(100).round(2)).reset_index()
    dataset.columns = ['valor', 'queda']

    chance_ativacao = dataset[dataset.valor >= minimo_ativacao].queda.sum()

    retorno = '\nChance de ativacao: {:.2f}%\n'.format(chance_ativacao)
    
    bar = ('[{}{}]'.format(''.ljust(int(chance_ativacao), '#'), ''.ljust(100 - int(chance_ativacao), '.')))

    return retorno+bar

def report_all():
    pass

# create folder if not exists
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == '__main__':
    create_folder(temp_dir)

    temp = os.listdir(temp_dir)

    dataset = gerar_dataset(arguments.roll, arguments.name)

    retorno = montar_retorno(dataset, arguments.minimo_ativacao)

    print(retorno)