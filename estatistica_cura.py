import os
import json
import argparse 
from utils import util
import pandas as pd
from prettytable import PrettyTable


# Definição de argumentos
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--name', default='Cura')
parser.add_argument('-r', '--roll', dest='roll', default=None)
parser.add_argument('-f', '--force_roll', dest='force_roll', action=argparse.BooleanOptionalAction)
parser.add_argument('-R', '--report', action=argparse.BooleanOptionalAction)
parser.add_argument('-F', '--save-file', action=argparse.BooleanOptionalAction)

arguments = parser.parse_args()

# Definição de constantes
vida_paladino   = 1716
vida_mago       = 936
amostra         = 100000
header_tabela   = ['Valor (pv)', '% Paladino', '% Mago', '% Queda', 'In 50%']
header_quartil  = ['Quartil', 'Valor']

temp = os.listdir('temp')

def gerar_dataset(roll, name):
    filename    = 'temp/{}.txt'.format(name)
    dataset     = {'roll': roll, 'amostra': amostra,'valores': []}

    for _ in range(amostra):
        dataset['valores'].append(util.roll(roll))

    with  open(filename, 'w') as file:
        file.write(json.dumps(dataset))

    del dataset

def montar_tabelas(name):
    dataset = json.load(open('temp/{}.txt'.format(name), 'r'))
    roll_string = dataset['roll']

    dataset = pd.Series(dataset['valores']).astype(int)

    quantile_group = dataset.quantile([0.25, 0.5, 0.75])

    #index as %
    quantile_group.index = quantile_group.index.map(lambda x: '{:.0f}%'.format(x * 100))

    #add max and min with named index
    quantile_group = quantile_group._append(pd.Series([dataset.max(), dataset.min()], index=['max', 'min']))
    quantile_group = quantile_group.astype(int)

    #Get 25 and 75 quartile
    quantile_25 = quantile_group['25%']
    quantile_75 = quantile_group['75%']

    tabela = (dataset.value_counts(normalize=True).mul(100).round(1).astype(str) + '%').sort_index(ascending=False)

    retorno = PrettyTable(header_tabela)
    for k, v in tabela.items():
        mago        = k / vida_mago * 100
        paladino    = k / vida_paladino * 100
        in_50       =  '*' if k >= quantile_25 and k <= quantile_75 else ''

        retorno.add_row(['{} {}'.format(k, in_50), '{:.2f}%'.format(paladino), '{:.2f}%'.format(mago), v, in_50])

    quartil = PrettyTable(header_quartil)
    for i, v in quantile_group.items():
        quartil.add_row([i, v])

    return retorno, quartil, roll_string

def beautify_name(name):
    return name.replace('_', ' ').upper() 

def report_all():

    files = os.listdir('temp')

    report_file_content = ''
    for file in files:
        nome = file.replace('.txt', '')
        retorno, quartil, roll_string = montar_tabelas(nome)

        report_file_content += str('\n\n{} ====================================\n\n'.format(beautify_name(nome)))
        report_file_content += str('\nRoll: {}'.format(roll_string))
        report_file_content += str('\n\nQuartis\n')
        report_file_content += str(quartil)
        report_file_content += str('\n\nTabela de cura\n')
        report_file_content += str(retorno)

    print(report_file_content)
    
    if arguments.save_file:
        with open('report/REPORT.txt', 'w') as file:
            file.write(report_file_content)

if __name__ == '__main__':

    if arguments.report:
        report_all()
        exit()

    if arguments.force_roll or '{}.txt'.format(arguments.name) not in temp:
        if arguments.roll is None:
            raise Exception('Argumento -r/--roll é obrigatório')
        gerar_dataset(arguments.roll, arguments.name)

    retorno, quartil, roll_string = montar_tabelas(arguments.name)
    print('\nQuartis')
    
    print(quartil)

    print('\nTabela de cura')
    print(retorno)

    print('\nRoll: {}'.format(roll_string))