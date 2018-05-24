""" Exceptions das consultas a API Inthegra """

class ItemNotFound(Exception):

    def __init__(self, message):
        self.message = message

