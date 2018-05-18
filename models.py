import datetime

class Route(object):
    """Representa uma Linha de Ônibus, conforme especificado na API Inthegra
    attributes:
    """

    def __init__(self, code, name, source_location, return_location, circular):
        self.code = code
        self.name = name
        self.source_location = source_location
        self.return_location = return_location
        self.circular = circular

    def __str__(self):
        return "Linha: %s, Nome: %s, Origem: %s, Retorno: %s, Circular: %r" % (self.code, self.name, self.source_location, self.return_location, self.circular)

    def bus_stops(self):
        return self.busstops


class BusStop(object):
    """ Representa uma parada de Onibus conforme a API Inthegra"""

    def __init__(self, code, name, address, latidude, longitude):
        self.code = code
        self.name = name
        self.address = address
        if not longitude is None:
            self.latidude = float(latidude)
            self.longitude = float(longitude)
            self.has_gps_location = True
        else:
            self.latidude = 0.0
            self.longitude = 0.0
            self.has_gps_location = False

    def __str__(self):
        return "Parada: %s, Nome: %s, Endereco: %s, Lat.: %f, Long.: %f" % (self.code, self.name, self.address, self.latidude, self.longitude)


class Bus(object):
    """ Representa um Onibus ativo no sistema de transito com sua posiacao atual

        Atributos:
        code -- inteiro, que representa o código da linha
        latidude, longitude -- float
        hour_str -- str represeting do hora
        hour -- datetime object from hour_str
    """

    def __init__(self, code, latidude, longitude, hour):
        self.code = int(code)
        self.latidude = float(latidude)
        self.longitude = float(longitude)
        self.hour_str = hour
        h, m, s = hour.split(':')
        self.hour = datetime.datetime.now().replace(hour=int(h), minute=int(m), second=int(s))

    def __str__(self):
        return "Bus: %d, , Lat.: %f, Long.: %f, Hora-str: %s, Hora: %s" % (self.code,
                                                                           self.latidude,
                                                                           self.longitude,
                                                                           self.hour_str,
                                                                           self.hour.strftime('%x %X'))

