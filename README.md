# 📌 Projet R5.A.12 – Algorithmes génétiques et application au problème du voyageur de commerce

## 📝 Description

Ce projet a pour objectif de mettre en œuvre un algorithme génétique afin de résoudre un problème d’optimisation complexe : le problème du voyageur de commerce (TSP).
Le TSP consiste à déterminer un chemin passant par un ensemble de villes exactement une fois chacune, puis revenant au point de départ, tout en minimisant la distance totale parcourue.

L’approche par algorithmes génétiques s’inspire du processus de sélection naturelle décrit par Darwin. Elle repose sur :

Une population initiale de solutions (chemins possibles).

Un processus d’évolution basé sur la sélection, le croisement et la mutation.

L’amélioration progressive des solutions au fil des générations.

## ⚙️ Fonctionnement de l’algorithme génétique

### Initialisation

Génération aléatoire d’une population de chemins valides (permutations des villes).

### Évaluation

Chaque individu est évalué en fonction de la longueur totale de son chemin.

Objectif : minimiser cette valeur.

### Sélection

Les meilleurs individus (chemins courts) sont privilégiés.

Méthodes possibles :

- Sélection par rang (choisir les meilleurs).

- Sélection par roulette (probabilité proportionnelle à la performance).

### Croisement

Deux individus (parents) échangent une partie de leur génome (sous-chemins).

Adaptation nécessaire pour conserver des permutations valides.

### Mutation

Un individu peut subir une petite modification (ex. inversion de deux villes).

Permet d’explorer de nouvelles solutions et d’éviter les minima locaux.

### Évolution

Répétition du cycle sur plusieurs générations.

git ckeckout develop
git pull origin develop
git checkout feature/…
git merge develop

commit push

git checkout develop
git merge feature/…

commit push

git checkout main
git pull origin main
git merge develop

commit push
