import json
import math

# Paramètres
INPUT_FILE = "maps/france_villes.json"
OUTPUT_FILE = "maps/france_villes_clean.json"
DIST_MIN_KM = 20  # Distance minimale entre deux villes (en km)
NB_VILLES_A_RETIRER = 50

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def load_villes(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["villes"]

def save_villes(villes, path):
    for i, v in enumerate(villes):
        v["id"] = i
    chemin = list(range(len(villes)))
    data = {"villes": villes, "chemin": chemin}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def filter_villes(villes, dist_min_km, nb_retirer):
    filtered = []
    for v in villes:
        lat, lon = v["coordonnees"]["latitude"], v["coordonnees"]["longitude"]
        trop_proche = False
        for vf in filtered:
            latf, lonf = vf["coordonnees"]["latitude"], vf["coordonnees"]["longitude"]
            if haversine(lat, lon, latf, lonf) < dist_min_km:
                trop_proche = True
                break
        if not trop_proche:
            filtered.append(v)
        if len(villes) - len(filtered) >= nb_retirer:
            continue
    # Si pas assez retiré, on coupe la liste
    if len(villes) - len(filtered) < nb_retirer:
        filtered = filtered[:len(villes)-nb_retirer]
    return filtered

def main():
    villes = load_villes(INPUT_FILE)
    villes_filtered = filter_villes(villes, DIST_MIN_KM, NB_VILLES_A_RETIRER)
    print(f"Villes initiales : {len(villes)} | Villes après filtrage : {len(villes_filtered)}")
    save_villes(villes_filtered, OUTPUT_FILE)
    print(f"Fichier sauvegardé : {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

