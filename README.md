# Développez une application Web en utilisant Django
*par Jean-Corentin Loirat*
le 20/05/2022

Lien du repository git hub : https://github.com/BeanEden/OC_Project_9

## Description de l'application :
Il s'agit d'un programme permettant la tenue de tournoi d'échec et la sauvegarde de ces informations (joueurs, tournois, rounds et matchs).
Ce tournoi comporte 8 joueurs et 4 tours.

L'ensemble des données (tournois, matchs, rounds et joueurs) est consultable de la base de données "database".json.
Les différentes instances sont stockées par table (une table "Tournament" pour les tournois "Player" pour les joueurs"...).

## Technologies :
* Django
* Python
* Html
* CSS

## Utilisation :

### 1 - Télécharger le dossier.zip :
Installez les élements dans le dossier de votre choix

### 2 - Créez un environement virtuel dans votre dossier et activez le :
* Commande terminal : `cd path/to/selected/project/directory`
* Commande terminal : `python -m venv env`
* Commande terminal : `env/Scripts/activate.bat` (sous Windows)

### 3 - Importez les packages :
Importez dans votre environnement virtuel les packages nécessaires à l'application.
* Commande terminal : `pip install -r requirements.txt`

### 4 - Lancez l'application : 
Lancez le serveur afin d'accéder au site.
* Commande terminal : `python manage.py runserver`


## Déroulement
Après avoir lancé le programme, l'utilisateur peut aller sur la page 
http://127.0.0.1:8000/

### Connexion : 
Si l'utilisateur n'est pas encore connecté, il peut :
* S'inscrire
* Se connecter

Si l'utilisateur est déjà connecté, il arrivera sur la page 
http://127.0.0.1:8000/home/

L'ensemble des pages du site requiert d'être connecté.

### Navigation : 

Fonctionnalités principales :
* Créer, gérer/ supprimer des tickets et des critiques
* S'abonner/ se désabonner à d'autres utilisateurs
* Consulter des feeds (tickets, critiques, utilisateurs)

## Database :
La base de donnée est le fichier `db.sqlite3`.

Les images sont stockées dans le dossier `media`

## En savoir plus :
Les fonctions et méthodes sont documentées via docstrings avec leurs utilisations, arguments et retours.


## Générer un report flake8:
Installez flake8 html

* Commande terminal : `pip install flake8-html`

Lancez le report flake8 avec une longueur de ligne de 119 caractères.
* Commande terminal :`flake8 --max-line-length=119 --format=html --htmldir=flake-report`

Un nouveau dossier flake-report est créé, contenant index.html.

## Contenu du repository git hub: 
* main.py
* Model Package
* Controller Package
* View Package
* requirements.txt
