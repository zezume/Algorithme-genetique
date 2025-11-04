def create_pile():
    return []

def ajouter_a_la_pile(pile, item):
    pile.append(item)

def retirer_de_la_pile(pile):
    if pile:
        return pile.pop()
    return None

def obtenir_taille_de_la_pile(pile):
    return len(pile)

def est_pile_vide(pile):
    return len(pile) == 0