import os
from dotenv import load_dotenv
from controllers.tool import create_villes_list, generer_population_aleatoire, evolution, OX, PMX, CX, load_villes_from_map_json

# Charger les variables d'environnement depuis le .env
load_dotenv("env.env")

# Récupérer les paramètres depuis le .env
CITIES_COUNT_ENV = os.getenv("CITIES_COUNT", "")
NOMBRE_VILLES = int(CITIES_COUNT_ENV) if CITIES_COUNT_ENV.strip() else None
TAILLE_POPULATION = int(os.getenv("POPULATION_SIZE", 50))
NB_GENERATIONS = int(os.getenv("GENERATIONS", 200))
TAUX_CROISEMENT = 0.8  # Non présent dans .env, valeur par défaut
TAUX_MUTATION = float(os.getenv("MUTATION_RATE", 0.01))
NB_ELITES = 2  # Non présent dans .env, valeur par défaut
CROSSOVER_METHOD = os.getenv("CROSSOVER_METHOD", "ox").lower()
MAP_FILE = os.getenv("MAP_FILE", "")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
OUTPUT_MAP_FILE = os.getenv("OUTPUT_MAP_FILE", "maps/output_map.json")

# Sélection de la méthode de croisement
if CROSSOVER_METHOD == "pmx":
    methode_croisement = PMX
elif CROSSOVER_METHOD == "cycle":
    methode_croisement = CX
else:
    methode_croisement = OX

# Générer les villes (ou charger depuis un fichier map si précisé)
if MAP_FILE:
    villes = load_villes_from_map_json(MAP_FILE)
else:
    villes = create_villes_list(NOMBRE_VILLES or 20)

# Générer la population initiale
population = generer_population_aleatoire(TAILLE_POPULATION, villes)

# Lancer l'évolution
meilleur = evolution(
    population,
    NB_GENERATIONS,
    TAUX_CROISEMENT,
    TAUX_MUTATION,
    NB_ELITES,
    methode_croisement,
    output_map_file=OUTPUT_MAP_FILE,
    show_plot_each_gen=True  # Affichage visuel à chaque génération
)

# Afficher le résultat
print("Meilleur chemin trouvé :")
chemin = []
courant = meilleur
while True:
    chemin.append(f"{courant.ville.nom} (id={courant.ville.id})")
    courant = courant.next
    if courant == meilleur:
        break
print(" -> ".join(chemin))
print(f"Distance totale : {meilleur.distance_totale():.2f}")
if DEBUG_MODE:
    print("Paramètres utilisés :")
    print(f"Population : {TAILLE_POPULATION}, Générations : {NB_GENERATIONS}, Mutation : {TAUX_MUTATION}, Croisement : {CROSSOVER_METHOD}")
print(f"Carte enregistrée dans : {OUTPUT_MAP_FILE}")

# Optionnel : afficher la carte (si implémenté dans view/affichage.py)
from view.affichage import afficher_chemin_json
afficher_chemin_json(OUTPUT_MAP_FILE)
