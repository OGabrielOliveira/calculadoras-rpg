import argparse

parser = argparse.ArgumentParser()
parser.add_argument("vida_base", type=int, nargs=1)
parser.add_argument("nivel", type=int, nargs=1)

args = parser.parse_args()

vida_base   = args.vida_base[0]
nivel       = args.nivel[0]

vida_total = vida_base

for i in range(1, nivel+1):
    vida_total += vida_base 
    
    vida_total = vida_total * 2 if i % 5 == 0 else vida_total

print('Vida total {} no Nv {}'.format(vida_total, nivel))