# InthegraAPI-STRANS-Python

**Classes Helper** em Python que demonstram o uso da API REST do Sistema de Transporte da STRANS/Teresina-PI, disponível em [Api Inthegra](https://inthegra.strans.teresina.pi.gov.br/)

### Status deste código
- **Em desenvolvimento**
- TODO List:
1. Repo local de itens como: Paradas e Rodas
2. Organizar classes/pacotes
3. Incluir novas funcionalidades que a Inthegra não disponibiliza
4. Disponibilizar uma API Wrapper da API Inthegra, com as novas funcionalidades
5. Fazer uma App de Uso dessas classes help

### Quer participar deste projeto comigo?
rogerio.silva at ifpi.edu.br


## Requisitos

- Python 3 (Para uso com Python 2.7, basta basta ajustar a função ```print``` no demo.py)
- Python Requests: 
```$ pip install requests```

## Demonstração de Uso

- Signin on Inthegra
```python
email = 'rogerio410@gmail.com'
password = ''
api_key = ''

token = InthegraAPI.signin(email, password, api_key)
```

- Obter de Linhas de Ônibus
```python
def test_linhas(str):
    linhas = InthegraAPI.routes(query=str)

    for l in linhas:
        print(l)

    print('Qtd de Linhas: ', linhas.__len__() )
```

- Obter Paradas de Ônibus
```python
def test_paradas(str):
    paradas = InthegraAPI.bus_stops(query=str)
    imprimir_paradas(paradas)


def test_paradas_por_linha(codigo_linha):
    linha, paradas = InthegraAPI.bus_stops_by_route_code(code=codigo_linha)
    print(linha)
    imprimir_paradas(paradas)


def imprimir_paradas(paradas):
    for p in paradas:
        print(p)
```

- Obter Posicionamento atual dos Ônibus no Sistema
```python
def test_posicao_veiculos_por_linha(codigo_linha):
    try:
        linha, onibus = InthegraAPI.bus_position_by_route_code(code=codigo_linha)
        print(linha)
        for o in onibus:
            print(o)
    except ItemNotFound as e:
        #API da STRAN pode não informar posições, o que pode gerar um exception
        print(e)
    except:
        print('Falha desconhecida')
```

