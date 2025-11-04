from faker import Faker
import random
import json

from model import coordonnees
from model.ville import Ville
from model.graphe import Graphe
from model.coordonnees import Coordonnee
from view.affichage import afficher_chemin_json
import time

fake =Faker()


def create_ville(id:int = 0, nom:str = "NomVille", coordonnees:tuple[float, float] = (0.0, 0.0)):
    return Ville(id, nom, Coordonnee(coordonnees[0], coordonnees[1]))

def create_villes_list(nombre_de_villes:int):
    villes = []
    for i in range(nombre_de_villes):
        ville = create_ville(id=i, nom=str(i), coordonnees=(random.randint(0, 100), random.randint(0, 100)))
        villes.append(ville)
    return villes

def create_graphe(villes: list[Ville]):
    if not villes:
        return None
    villes = [v for v in villes if v is not None]
    tete = Graphe(villes[0])
    courant = tete
    for ville in villes[1:]:
        nouveau_noeud = Graphe(ville)
        courant.set_next(nouveau_noeud)
        courant = nouveau_noeud
    courant.set_next(tete)
    return tete


def generer_population_aleatoire(taille_population: int, liste_ville: list[Ville]):
    population = []
    for _ in range(taille_population):
        individu = liste_ville[0:1]  # Garder la première ville fixe
        reste = liste_ville[1:].copy()
        random.shuffle(reste)
        individu.extend(reste)
        population.append(create_graphe(individu))
    return population

# Sélection
def selection_par_rang(population: list[Graphe], taille_selection: int):
    # Trier la population par fitness (distance totale)
    population_triee = sorted(population, key=lambda x: x.distance_totale())
    # Sélectionner les meilleurs individus
    return population_triee[:taille_selection]


# Croisement
def OX(parent1: Graphe, parent2: Graphe) -> Graphe:
    def graphe_to_list(graphe: Graphe):
        villes = []
        current = graphe
        while True:
            villes.append(current.ville)
            current = current.next
            if current == graphe:
                break
        return villes

    liste1 = graphe_to_list(parent1)
    liste2 = graphe_to_list(parent2)
    taille = len(liste1)
    debut, fin = sorted(random.sample(range(1, taille), 2))  # Éviter la première ville

    enfant = [None] * taille
    enfant[0] = liste1[0]
    enfant[debut:fin] = liste1[debut:fin]

    current_index = fin
    for ville in liste2:
        if ville not in enfant:
            if current_index >= taille:
                current_index = 1  # Revenir au début en évitant la première ville
            enfant[current_index] = ville
            current_index += 1
    for i in range(taille):
        if enfant[i] is None:
            for ville in liste2:
                if ville not in enfant:
                    enfant[i] = ville
                    break
    return create_graphe(enfant)

def CX(parent1: Graphe, parent2: Graphe) -> Graphe:
    def graphe_to_list(graphe: Graphe):
        villes = []
        current = graphe
        while True:
            villes.append(current.ville)
            current = current.next
            if current == graphe:
                break
        return villes

    liste1 = graphe_to_list(parent1)
    liste2 = graphe_to_list(parent2)
    taille = len(liste1)
    enfant = [None] * taille
    enfant[0] = liste1[0]
    villes_ajoutees = {liste1[0]}

    index = 1
    while None in enfant:
        if liste1[index] not in villes_ajoutees:
            enfant[index] = liste1[index]
            villes_ajoutees.add(liste1[index])
        elif liste2[index] not in villes_ajoutees:
            enfant[index] = liste2[index]
            villes_ajoutees.add(liste2[index])
        index += 1
        if index >= taille:
            index = 1
    for i in range(taille):
        if enfant[i] is None:
            for ville in liste2:
                if ville not in enfant:
                    enfant[i] = ville
                    break
    return create_graphe(enfant)

def PMX(parent1: Graphe, parent2: Graphe) -> Graphe:
    def graphe_to_list(graphe: Graphe):
        villes = []
        current = graphe
        while True:
            villes.append(current.ville)
            current = current.next
            if current == graphe:
                break
        return villes

    liste1 = graphe_to_list(parent1)
    liste2 = graphe_to_list(parent2)
    taille = len(liste1)
    debut, fin = sorted(random.sample(range(1, taille), 2))

    enfant = [None] * taille
    enfant[0] = liste1[0]
    enfant[debut:fin] = liste1[debut:fin]

    mapping = {}
    for i in range(debut, fin):
        mapping[liste2[i]] = liste1[i]

    for i in range(1, taille):
        if debut <= i < fin:
            continue
        ville = liste2[i]
        while ville in mapping:
            ville = mapping[ville]
        enfant[i] = ville
    for i in range(taille):
        if enfant[i] is None:
            for ville in liste2:
                if ville not in enfant:
                    enfant[i] = ville
                    break
    return create_graphe(enfant)

# Mutation

def mutation(individu: Graphe, taux_mutation: float):
    if random.random() < taux_mutation:
        # Convertir le graphe en liste pour faciliter la manipulation
        villes = []
        current = individu
        while True:
            villes.append(current.ville)
            current = current.next
            if current == individu:
                break

        # Sélectionner deux indices aléatoires à échanger (en évitant la première ville)
        idx1 = random.randint(1, len(villes) - 1)
        idx2 = random.randint(1, len(villes) - 1)

        # Échanger les villes aux indices sélectionnés
        villes[idx1], villes[idx2] = villes[idx2], villes[idx1]

        # Recréer le graphe avec l'ordre modifié
        return create_graphe(villes)
    return individu


# Évaluation
def fitness(individu: Graphe) -> float:
    return individu.distance_totale()

# Sélection par tournoi
def selection_tournoi(population: list[Graphe], fitnesses: list[float], k: int = 3) -> Graphe:
    participants = random.sample(list(zip(population, fitnesses)), k)
    participants.sort(key=lambda x: x[1])
    return participants[0][0]

# Sélection des E meilleurs (élitisme)
def selection_elites(population: list[Graphe], fitnesses: list[float], nb_elites: int) -> list[Graphe]:
    elites = sorted(zip(population, fitnesses), key=lambda x: x[1])[:nb_elites]
    return [e[0] for e in elites]

def evolution(
    population: list[Graphe],
    nb_generations: int,
    taux_croisement: float,
    taux_mutation: float,
    nb_elites: int,
    methode_croisement,
    output_map_file: str = None,
    show_plot_each_gen: bool = False
) -> Graphe:
    taille_population = len(population)
    meilleur_fitness_prec = None
    meilleur_chemin_prec = None
    start_time = time.time()
    for g in range(nb_generations):
        # Évaluation
        fitnesses = [fitness(ind) for ind in population]
        meilleur_index = fitnesses.index(min(fitnesses))
        meilleur = population[meilleur_index]
        # Construction du chemin du meilleur
        chemin_ids = []
        courant = meilleur
        while True:
            chemin_ids.append(str(courant.ville.id))
            courant = courant.next
            if courant == meilleur:
                break
        meilleur_fitness = min(fitnesses)
        current_time = time.time() - start_time
        # Affichage seulement si le meilleur change
        if meilleur_fitness != meilleur_fitness_prec or chemin_ids != meilleur_chemin_prec:
            print(f"Génération {g+1}/{nb_generations} | Meilleur: {meilleur_fitness:.2f} | Temps: {current_time:.2f}s | Chemin: {' -> '.join(chemin_ids)}")
            if show_plot_each_gen and output_map_file:
                export_map_json(meilleur, output_map_file)
                afficher_chemin_json(output_map_file, show_plot=True)
            meilleur_fitness_prec = meilleur_fitness
            meilleur_chemin_prec = list(chemin_ids)
        nouvelle_population = []
        # Élitisme
        elites = selection_elites(population, fitnesses, nb_elites)
        nouvelle_population.extend(elites)
        # Génération des nouveaux individus
        while len(nouvelle_population) < taille_population:
            parent1 = selection_tournoi(population, fitnesses)
            parent2 = selection_tournoi(population, fitnesses)
            if random.random() < taux_croisement:
                enfant1 = methode_croisement(parent1, parent2)
                enfant2 = methode_croisement(parent2, parent1)
            else:
                enfant1 = parent1
                enfant2 = parent2
            if random.random() < taux_mutation:
                enfant1 = mutation(enfant1, taux_mutation)
            if random.random() < taux_mutation:
                enfant2 = mutation(enfant2, taux_mutation)
            nouvelle_population.append(enfant1)
            if len(nouvelle_population) < taille_population:
                nouvelle_population.append(enfant2)
        population = nouvelle_population[:taille_population]
    # Dernière évaluation
    fitnesses = [fitness(ind) for ind in population]
    meilleur_index = fitnesses.index(min(fitnesses))
    meilleur = population[meilleur_index]
    total_time = time.time() - start_time
    # Export map si demandé
    if output_map_file:
        export_map_json(meilleur, output_map_file)
    print(f"\nTemps total d'exécution : {total_time:.2f} secondes")
    return meilleur

def export_map_json(graphe: Graphe, file_path: str):
    villes = []
    chemin = []
    courant = graphe
    deja_vus = set()
    while True:
        ville = courant.ville
        if ville.id in deja_vus:
            break
        villes.append({
            "id": ville.id,
            "nom": ville.nom,
            "coordonnees": {
                "latitude": ville.coordonnees.latitude,
                "longitude": ville.coordonnees.longitude
            }
        })
        chemin.append(ville.id)
        deja_vus.add(ville.id)
        courant = courant.next
        if courant == graphe:
            break
    data = {
        "villes": villes,
        "chemin": chemin
    }
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_villes_from_map_json(json_path: str) -> list[Ville]:
    """
    Charge une liste de villes à partir d'un fichier JSON (format export_map_json).
    """
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    villes = []
    for v in data["villes"]:
        ville = Ville(
            id=v["id"],
            nom=v["nom"],
            coordonnees=Coordonnee(
                v["coordonnees"]["latitude"],
                v["coordonnees"]["longitude"]
            )
        )
        villes.append(ville)
    return villes
