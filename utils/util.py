import re
import random 

def rolagens(roll):
    rolls, limit = 1, 0
    results = []
    mods = []
    parts = roll.split('+')

    result_str = []
    for part in parts:
        if 'd' in part:
            r, l = map(str, part.split('d'))

            rolls, limit = int(r) if r else 1, int(l)
            result = [random.randint(1, limit) for _ in range(rolls)]
            result.sort(reverse=True)
            results.append(result)

            result_str.append('{} {}d{}'.format('[' + ', '.join(str(r) for r in result) + ']', rolls, limit))
        else:
            mods.append(int(part))

    total = sum(sum(result) for result in results) + sum(mods)
    result_str = ' + '.join(result_str)

    if mods:
        mod_str = ' + '.join(str(mod) for mod in mods)
        result_str += ' + ' + mod_str
    return total 

def parser_roll(roll):
    partes = re.split(r'(\+|\-|\\|\*|\(|\))', roll)
    partes = [x.strip() for x in partes if x not in ('', ' ')]

    for i in range(len(partes)):
        if 'd' in partes[i]:
            partes[i] = rolagens(partes[i])
    partes = [str(x) for x in partes]

    return eval(''.join(partes))

def roll(roll):
    qtd_rolls = roll.split('#')

    rolls = qtd_rolls[1] if 1 in range(len(qtd_rolls)) else qtd_rolls[0]
    qtd   = int(qtd_rolls[0]) if 1 in range(len(qtd_rolls)) else 1

    retorno = []
    for n in range(0, qtd):
        retorno.append(parser_roll(rolls))

    return retorno[0]
