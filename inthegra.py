import requests
import json
import datetime
from models import Route, BusStop, Bus
from exceptions import ItemNotFound


class Token(object):

    def __init__(self, token='', minutes=10):
        self.token = token
        self.minutes = minutes

    def __str__(self):
        return 'Token: %s, Minutes: %s' % (self.token, self.minutes)


class InthegraAPI(object):
    """Representa a API Inthegra da STRANS Teresina-PI
    Attributes:
        url
        email
        password
        api_key
    """

    url = 'https://api.inthegra.strans.teresina.pi.gov.br/v1'
    api_key = ''
    token = Token()

    @classmethod
    def signin(cls, email, password, api_key):
        cls.email = email
        cls.password = password
        cls.api_key = api_key

        payload = {'email': cls.email,
                   'password': cls.password}

        result = requests.post(cls.url+'/signin', data=json.dumps(payload), headers=cls.__get_headers())

        if result.status_code == 200:
            cls.token = Token(result.json()['token'], result.json()['minutes'])
            print(cls.token)
            return cls.token
        else:
            result.raise_for_status()

    @classmethod
    def __get_headers(cls):
        headers = {'Content-Type': 'application/json',
                   'Accept-Language': 'en',
                   'Date': datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
                   'X-Api-Key': InthegraAPI.api_key
                   }
        return headers

    @classmethod
    def current_token(cls):
        return cls.token

    @classmethod
    def routes(cls, query=""):
        """ Retorna todas as linhas que possuam o termo “ininga” na denominação,
            no ponto de origem ou ponto de retorno. """

        headers = cls.__get_headers()
        headers['X-Auth-Token'] = cls.token.token

        #Faz chamada pelas linhas
        result = requests.get(cls.url + '/linhas?busca='+query, headers=headers)

        linhas = []

        if  result.status_code == 200:
            for linha in result.json():
                route = Route(code=linha.get('CodigoLinha'),
                              name=linha.get('Denomicao'),
                              source_location=linha.get('Origem'),
                              return_location=linha.get('Retorno'),
                              circular=linha.get('Circular'))
                linhas.append(route)
            return linhas
        else:
            print(result.json()['code'], result.json()['message'])

    @classmethod
    def bus_stops(cls, query=""):
        """ Retorna todas as paradas que possuam o termo “ininga” na denominação ou no endereço. """

        headers = cls.__get_headers()
        headers['X-Auth-Token'] = cls.token.token

        url = cls.url + '/paradas?busca=' + query

        # Faz chamada pelas paradas
        result = requests.get(url, headers=headers)

        paradas = []

        if result.status_code == 200:
            for parada in result.json():
                bus_stop = BusStop(code=parada.get('CodigoParada'),
                                 name=parada.get('Denomicao'),
                                 address=parada.get('Endereco'),
                                 latidude=parada.get('Lat'),
                                 longitude=parada.get('Long'),
                                 )
                paradas.append(bus_stop)
            return paradas
        else:
            print(result.json()['code'], result.json()['message'])

    @classmethod
    def bus_stops_by_route_code(cls, code):

        """ Retorna todas as paradas da linha indicada. """

        headers = cls.__get_headers()
        headers['X-Auth-Token'] = cls.token.token

        url = cls.url + '/paradasLinha?busca=' + code

        # Faz chamada pelas paradas
        result = requests.get(url, headers=headers)

        paradas = []

        if result.status_code == 200:
            # A Linha
            linha = result.json()['Linha']
            route = Route(code=linha.get('CodigoLinha'),
                          name=linha.get('Denomicao'),
                          source_location=linha.get('Origem'),
                          return_location=linha.get('Retorno'),
                          circular=linha.get('Circular'))
            # As Paradas da Linha
            for parada in result.json()['Paradas']:
                bus_stop = BusStop(code=parada.get('CodigoParada'),
                                 name=parada.get('Denomicao'),
                                 address=parada.get('Endereco'),
                                 latidude=parada.get('Lat'),
                                 longitude=parada.get('Long'),
                                 )
                paradas.append(bus_stop)

            return route, paradas
        else:
            print(result.json()['code'], result.json()['message'])
            raise ItemNotFound('Nao ha paradas disponiveis')

    @classmethod
    def bus_position_by_route_code(cls, code):
        """ bus_position_by_route_code(code) -> route, list of buses """

        headers = cls.__get_headers()
        headers['X-Auth-Token'] = cls.token.token

        url = cls.url + '/veiculosLinha?busca=' + code

        # Faz chamada pelas paradas
        result = requests.get(url, headers=headers)

        buses = []

        if result.status_code == 200:
            # A Linha
            linha = result.json()['Linha']
            route = Route(code=linha.get('CodigoLinha'),
                          name=linha.get('Denomicao'),
                          source_location=linha.get('Origem'),
                          return_location=linha.get('Retorno'),
                          circular=linha.get('Circular')
                          )
            # Os Veiculos da Linha
            for onibus in linha.get('Veiculos'):
                bus = Bus(code=onibus.get('CodigoVeiculo'),
                               latidude=onibus.get('Lat'),
                               longitude=onibus.get('Long'),
                               hour=onibus.get('Hora')
                          )
                buses.append(bus)

            return route, buses
        else:
            print(result.json()['code'], result.json()['message'])
            raise ItemNotFound('Nao há veiculos circulação disponiveis')