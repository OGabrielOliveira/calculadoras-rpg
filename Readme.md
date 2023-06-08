# Calculadoras do sistema de RPG Iteralis

Conjunto de scripts para simplificar os calculos do sistema de RPG Iteralis

## calculo_vida.py

Realiza utiliza o nivel e a vida base para realizar o calculo da vida total dos personagens

Ex de uso:
```bash
python calculo_vida.py {vida por nivel} {nivel}
```


## estatistica_cura.py

Cria um relatorio de probabilidades dos dados de cura do sistema

Ex de uso:
```bash
python estatistica_cura.py -t cura -r "3 * (2d4 + d5)"
```