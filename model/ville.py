from model import *


class Ville:
    def __init__(self, id:int, nom:str , coordonnees:Coordonnee):
        self.id = id
        self.nom = nom
        self.coordonnees = coordonnees

    def __str__(self):
        return f"Ville(id={self.id}, nom={self.nom}, {self.coordonnees})"
