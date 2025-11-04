from model.ville import Ville




class Graphe:
    def __init__(self,ville:Ville, next=None):
        self.ville = ville
        self.next = next
        self.distance = None

    def set_next(self, graphe):
        self.next = graphe
        self.distance = self.ville.coordonnees.distance(graphe.ville.coordonnees)
        return self.next

    def distance(self):
        return self.distance

    def distance_totale(self):
        total_distance = 0
        current = self
        start = self
        if not current:
            return 0
        while True:
            if current.next:
                total_distance += current.distance
                current = current.next
            else:
                break
            if current == start:
                break
        if current.ville != start.ville:
            total_distance += current.ville.coordonnees.distance(start.ville.coordonnees)
        return total_distance

    def __str__(self):
        next_ville = self.next.ville.nom if self.next else "None"
        return f"Graphe(ville={self.ville}, next={next_ville})"