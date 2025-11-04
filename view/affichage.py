import json
import matplotlib.pyplot as plt

def afficher_chemin_json(json_path: str, show_plot: bool = True, save_path: str = None):
    """
    Affiche le chemin optimal à partir d'un fichier JSON exporté par l'algorithme génétique.
    Peut aussi sauvegarder l'image si save_path est fourni.
    """
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    villes = {v['id']: v for v in data['villes']}
    chemin = data['chemin']

    # Extraire les coordonnées dans l'ordre du chemin
    x = [villes[vid]['coordonnees']['longitude'] for vid in chemin]
    y = [villes[vid]['coordonnees']['latitude'] for vid in chemin]
    noms = [villes[vid]['nom'] for vid in chemin]

    plt.figure(figsize=(8, 8))
    plt.plot(x, y, '-o', color='blue', label='Chemin')
    for i, (xi, yi, nom) in enumerate(zip(x, y, noms)):
        plt.text(xi, yi, f"{nom}", fontsize=9, ha='right', va='bottom', color='red')
    plt.scatter(x, y, color='green', zorder=5)
    plt.title("Chemin optimal trouvé (Algorithme génétique)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    if show_plot:
        plt.show()
    plt.close()
