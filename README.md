# OPTILUX Desktop

Application de bureau (pas un site web) pour la gestion d'OPTILUX :
clients & prescriptions, rendez-vous, stock, ventes, dépenses, utilisateurs.

- Fonctionne **entièrement hors ligne**.
- Les données sont stockées dans un vrai fichier de base de données SQLite
  (`optilux.db`), créé automatiquement à côté de `app.py` au premier lancement.
- Deux niveaux d'accès : **Administrateur** (tout) et **Employé**
  (clients, rendez-vous, stock, ventes — pas les dépenses, pas les utilisateurs).

## Installation (à faire une seule fois)

### 1. Installer Python
S'il n'est pas déjà installé :
- **Windows** : télécharger sur https://www.python.org/downloads/ — pendant
  l'installation, cocher la case **"Add Python to PATH"**.
- **Mac** : télécharger sur https://www.python.org/downloads/macos/

### 2. Installer la dépendance (génération des factures PDF)
Ouvrir un terminal (**Invite de commandes** sur Windows, **Terminal** sur Mac)
dans le dossier de l'application, puis :

```
pip install -r requirements.txt
```

Sur Mac, si `pip` n'est pas reconnu, essayer `pip3` à la place.

## Lancer l'application

Dans le même terminal, dans le dossier de l'application :

```
python app.py
```

(sur Mac : `python3 app.py`)

Une fenêtre s'ouvre avec l'écran de connexion.

## Comptes de démonstration

| Rôle          | Identifiant | Mot de passe |
|---------------|-------------|--------------|
| Administrateur| admin       | admin123     |
| Employé       | employe1    | employe123   |

Vous pouvez changer ces mots de passe et créer d'autres comptes depuis
l'onglet **Utilisateurs** (visible uniquement pour l'administrateur).

## Dossier `assets/`

Contient le logo (`optilux_logo.png`) et l'icône de l'application
(`optilux.ico`). Gardez ce dossier à côté de `app.py` — c'est ce qui affiche
le logo dans la barre latérale, sur l'écran de connexion, et l'icône de la
fenêtre / barre des tâches (sous Windows).

## Derniers ajustements

- **Écran de connexion** : corrigé pour le mode sombre — avant, seuls les
  champs de saisie changeaient de couleur, ce qui donnait un rendu bizarre ;
  maintenant toute la fenêtre (carte, textes, champs) suit le thème choisi.
- **Commandes fournisseur** : nouvel onglet "Commandes fournisseur (stock)"
  à côté de "Commandes clients", pour suivre vos propres commandes de
  réapprovisionnement (montures, verres…) séparément des commandes clients.
- **Logo** : agrandi dans la barre latérale et l'écran de connexion.
- **Transition entre les pages** : le texte (titres, boutons, tableaux) de
  la nouvelle page apparaît en fondu à chaque changement de page — la
  fenêtre elle-même reste toujours parfaitement opaque, vous ne voyez jamais
  le bureau Windows à travers l'application.

## Nouveautés — grosse mise à jour

- **Fiche client** entièrement refaite pour correspondre à votre fiche papier :
  identité (Nom/Prénom/Né(e) le/Ville/Num), E.F.H (VL/VP/PG), ARX, AV. Brute,
  Prescripteur, Mutuelle, Maladie, **Montage** (Oui/Non comme les autres),
  tableau SPH/CYL/AXE/ADD/EP/HT pour OD et OG, Verres/Firme/Monture, Prix/Avance,
  jour de livraison (L/ME/MA/J/V/S), et le champ R.
- **Remise client** : 5 à 100%, reportée automatiquement sur une nouvelle vente
  pour ce client (modifiable au cas par cas).
- **Ventes** : mode de paiement (Espèces / TPE) par vente, avec un total
  Espèces et un total TPE affichés en haut de la page.
- **Dépenses** : bascule "Charges (entreprise)" / "Dépenses personnelles",
  et un champ "Échéance" pour recevoir un rappel avant la date limite.
- **Stock** : photo du produit (fichier image), et pour la catégorie
  "Lentilles" spécifiquement, le type (souples/rigides/couleur…) et la durée
  de port (1 jour, 1 mois, etc.) apparaissent automatiquement.
- **Types & Produits** (nouvel onglet, admin) : ajoutez ou supprimez vous-même
  les catégories, marques, types et durées de lentilles — elles apparaissent
  aussitôt dans les menus déroulants correspondants, sans toucher au code.
- **Commandes** (nouvel onglet) : suivez les commandes en cours par client,
  avec une alerte "BIENTÔT" (échéance proche) ou "EN RETARD" directement
  dans le tableau, et une notification Windows quand une commande approche.
- **Recherche** ajoutée sur tous les tableaux (Clients, Rendez-vous, Stock,
  Ventes, Dépenses, Commandes, Journal d'activité).
- **Rappels de charges** : notification Windows 3 jours avant l'échéance
  d'une dépense, puis le jour même.

## Nouveautés d'interface

- **Écran de démarrage** : le logo (verres) apparaît en fondu, avec une
  silhouette de l'application qui se dessine, le temps que tout se prépare.
- **Survol animé** : boutons et menu latéral réagissent avec une transition
  douce (pas un changement de couleur brutal).
- **Icônes** : chaque bouton, chaque page du menu, et les cartes du tableau
  de bord ont une icône dédiée (dessinée par le programme lui-même — pas des
  emojis, pour un rendu identique et fiable sur toutes les machines Windows).
- **Barre de défilement** : personnalisée aux couleurs OPTILUX (rouge/blanc)
  sur les tableaux et les fenêtres d'ajout/modification.
- **Fenêtres d'ajout/modification** : le contenu défile désormais si le
  formulaire est plus long que l'écran (ex. fiche client avec prescription
  complète) — les boutons Enregistrer/Annuler restent toujours visibles en
  bas, ils ne défilent jamais hors de vue.
- **Mode sombre / clair** : bouton en bas du menu (icône lune/soleil).
  Le menu latéral reste toujours foncé (identité visuelle), seul l'espace
  de travail change. Le choix est mémorisé et repris au prochain lancement.
- **Icône de l'application** : les verres rouges apparaissent dans la barre
  des tâches Windows, la fenêtre, et les fenêtres d'ajout/modification.

## Notifications Windows

L'application envoie des notifications système (bulle Windows) pour :
- **Rendez-vous à venir** — dans les 15 minutes précédant l'heure du RDV.
- **Stock faible** — un résumé à la connexion, et immédiatement après avoir
  modifié un article dont la quantité passe sous le seuil d'alerte.
- **Rappel de charge** — 3 jours avant l'échéance d'une dépense, puis le jour même.
- **Commandes à suivre** — quand une commande approche de sa date prévue ou
  est en retard.

**Important** : les notifications ne fonctionnent que pendant que
l'application est ouverte et que vous êtes connecté — ce n'est pas un
service qui tourne en arrière-plan sur Windows. Si l'application est fermée,
aucune notification ne sera envoyée. Si vous avez besoin de rappels même
application fermée, cela nécessiterait un service Windows séparé — dites-le
moi si c'est utile pour vous.

## Vos données

Tout est stocké dans `optilux.db`, dans ce même dossier. C'est un vrai fichier
sur votre ordinateur — pas de cloud, pas de compte, pas d'internet requis pour
l'utiliser au quotidien.

**Sauvegarde recommandée** : copiez de temps en temps le fichier `optilux.db`
(par exemple sur une clé USB ou dans un dossier partagé) au cas où
l'ordinateur aurait un problème. Si vous supprimez ce fichier, vous repartez
de zéro au prochain lancement.

Les factures PDF générées sont enregistrées dans le sous-dossier `factures/`.

## Important à savoir

- Cette version fonctionne sur **un seul ordinateur à la fois**. Si vous
  voulez que plusieurs postes (ex. comptoir + bureau) partagent les mêmes
  données en temps réel, il faut une version avec une base de données
  centralisée sur un serveur — c'est un projet différent, dites-le moi si
  vous en avez besoin.
- Les mots de passe sont maintenant correctement chiffrés dans la base de
  données (contrairement à la version web précédente), mais rappelez-vous
  que n'importe qui ayant un accès physique à l'ordinateur et au compte
  Windows/Mac peut ouvrir l'application. Pour une vraie séparation des
  accès (ex. protéger les finances même d'un employé qui a accès à
  l'ordinateur), il faudrait des comptes Windows/Mac séparés en plus.
- Je n'ai pas pu créer d'installeur cliquable (.exe / .app) depuis mon
  environnement — celui-ci doit être généré sur votre propre ordinateur
  (avec un outil comme PyInstaller). Je peux vous guider pour ça si vous
  voulez une version "double-clic, sans terminal".

## Créer un raccourci sans terminal (optionnel)

Une fois que tout fonctionne avec `python app.py`, on peut générer un vrai
`.exe` (Windows) ou `.app` (Mac) avec PyInstaller, pour double-cliquer et
lancer l'application sans passer par le terminal. Demandez-moi si vous
voulez les étapes.
