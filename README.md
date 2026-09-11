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

## Dernière mise à jour

- **Lisibilité** : toutes les polices agrandies dans toute l'application
  (menu, tableaux, boutons, formulaires) pour une lecture plus confortable.
  La barre latérale et les lignes des tableaux ont été élargies en
  conséquence pour que rien ne soit coupé.
- **Facture refaite à l'identique** de votre vraie facture papier : les deux
  logos OPTILUX, Vision de LOIN / ADD Vision de PRES, les cases VL/VP/PROGRESSIF,
  le tableau Désignation/Prix unité/Montant TTC, Cachet et signature + TOTAL TTC,
  le montant en toutes lettres, et le pied de page avec vos informations légales.
- **Facture en Word (.docx)**, en plus du PDF — un bouton "Facture Word" à
  côté de "Facture PDF" dans Ventes. Les deux formats sont conservés
  séparément (générer l'un n'efface pas l'autre).
- **Rangement des factures** (nouvel onglet "Factures") : toutes les
  factures générées depuis une vente y apparaissent automatiquement, et vous
  pouvez aussi en ajouter manuellement (avec un fichier PDF/image/Word joint).
  Séparées en deux : **Factures clients** et **Factures de l'entreprise**
  (ex. vos propres factures fournisseurs).
- **Tableau de bord enrichi** : nouvelle carte "Commandes à suivre" (visible
  par tous), et "Factures récentes" (administrateur). Les cartes du bas sont
  passées de 3 à 2 par rangée pour laisser respirer le texte agrandi.
- **Correction** : le petit indicateur "photo" du Stock qui s'affichait
  parfois comme un carré illisible (rendu incompatible avec certaines
  polices Windows) a été remplacé par du texte simple ("Oui"/"—").
- **Rappels WhatsApp automatiques (gratuit)** : voir la section dédiée
  ci-dessous.

## WhatsApp automatique (gratuit)

Utilise `pywhatkit` — pas de clé API, pas de compte professionnel Meta.

- **Automatique** : quand un rappel de rendez-vous se déclenche (15 minutes
  avant), si le client a un numéro de téléphone enregistré dans sa fiche,
  un message WhatsApp lui est envoyé en plus de la notification Windows.
- **Manuel** : bouton "Envoyer rappel WhatsApp" dans Rendez-vous, pour
  envoyer à la demande sur le rendez-vous sélectionné.

**Important à savoir avant d'utiliser cette fonctionnalité :**
- Il faut que WhatsApp Web soit déjà connecté sur l'ordinateur (scan du QR
  code une seule fois — la session reste active ensuite).
- Une fenêtre de navigateur s'ouvre VISIBLEMENT à chaque envoi — ce n'est
  pas silencieux comme les notifications Windows.
- Ce n'est pas un canal officiel WhatsApp. Réservez ceci à des rappels
  ponctuels, pas à un envoi en masse — un envoi trop fréquent peut faire
  limiter temporairement le numéro par WhatsApp.
- Les numéros marocains locaux (ex. 0612345678) sont convertis
  automatiquement au format international (+212612345678).

## Dernière mise à jour (2)

- **Correction d'un vrai bug** : la fiche client s'affichait tronquée (quelques
  champs seulement, puis plus rien) dès qu'un client avait une info manquante
  (date de naissance, ville ou téléphone vides). C'était un plantage silencieux
  au moment de préremplir le champ — corrigé à la racine, ça ne peut plus
  arriver nulle part dans l'application.
- **Fiche client et fiche produit** : ouvrir un client ou un article (double-clic,
  ou bouton "Voir la fiche") affiche maintenant une fiche de consultation
  propre et en lecture seule — plus de risque de modifier une info par erreur.
  Un bouton "Modifier" explicite ouvre ensuite le vrai formulaire d'édition.
  La fiche produit affiche la photo en grand en haut, comme demandé.
- **Calendrier (.ics)** : bouton "Exporter calendrier" sur le tableau de bord.
  Regroupe tous les rendez-vous et commandes à venir dans un fichier
  standard que Google Agenda et l'application Calendrier Samsung savent
  ouvrir directement. Voir la section dédiée ci-dessous.

## Calendrier sur votre téléphone (Samsung)

Le bouton **"Exporter calendrier (.ics)"** sur le tableau de bord crée un
fichier contenant tous les rendez-vous et commandes à venir.

**Comment le voir sur votre téléphone :**
1. Cliquez sur le bouton, choisissez où l'enregistrer (par exemple dans un
   dossier Google Drive ou OneDrive s'il est installé sur l'ordinateur —
   sinon n'importe où, puis envoyez-le-vous par e-mail).
2. Sur votre téléphone, ouvrez ce fichier (depuis l'e-mail, ou l'app Google
   Drive/OneDrive, ou en le transférant par USB/Bluetooth).
3. Le téléphone propose de l'ajouter à **Google Agenda** ou au
   **Calendrier Samsung** — les événements apparaissent avec un rappel
   30 minutes avant.

**Important à savoir** : ce n'est **pas** une synchronisation automatique en
continu — c'est un export que vous relancez de temps en temps (par exemple
chaque matin, ou une fois par semaine) pour que le téléphone reste à jour.
Une vraie synchronisation automatique (les nouveaux RDV apparaissent seuls
sur le téléphone sans réexporter) est possible mais demande de connecter
l'application à un compte Google — un projet plus important, à faire si
cette fonctionnalité s'avère utile au quotidien.

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
