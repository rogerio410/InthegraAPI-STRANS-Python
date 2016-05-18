from inthegra import InthegraAPI
from exceptions import ItemNotFound

email = 'rogerio410@gmail.com'
password = ''
api_key = ''

token = InthegraAPI.signin(email, password, api_key)


def test_linhas(str):
    linhas = InthegraAPI.routes(query=str)

    for l in linhas:
        print(l)

    print('Qtd de Linhas: ', linhas.__len__() )


def test_paradas(str):
    paradas = InthegraAPI.bus_stops(query=str)
    imprimir_paradas(paradas)


def test_paradas_por_linha(codigo_linha):
    try:
        linha, paradas = InthegraAPI.bus_stops_by_route_code(code=codigo_linha)
        print(linha)
        imprimir_paradas(paradas)
    except ItemNotFound as e:
        print(e)
    except:
        print('Falha desconhecida')


def test_posicao_veiculos_por_linha(codigo_linha):
    try:
        linha, onibus = InthegraAPI.bus_position_by_route_code(code=codigo_linha)
        print(linha)
        for o in onibus:
            print(o)
    except ItemNotFound as e:
        print(e)
    except:
        print('Falha desconhecida')


def imprimir_paradas(paradas):
    for p in paradas:
        print(p)

    print('Qtd de Paradas', paradas.__len__())


# Descomente as linhas abaixo para testa as funcionalidades.

#test_linhas('Baix')
#test_paradas('1200')
#test_paradas_por_linha('0505')
test_posicao_veiculos_por_linha('0505')