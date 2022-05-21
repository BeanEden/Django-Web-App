# Développez une application Web en utilisant Django
*par Jean-Corentin Loirat*
le 20/05/2022

Lien du repository git hub : https://github.com/BeanEden/OC_Project_9

## Description de l'application :
Application web "LITReview" permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande.

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

### 4 - Vérifiez les migrations : 
Vérifiez que les migrations sont sont bien à jour
* Commande terminal : `python manage.py makemigrations`
* Commande terminal : `python manage.py migrate`

### 5 - Lancez l'application : 
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
http://127.0.0.1:8000/home/ \
L'ensemble des pages du site requiert d'être connecté.

### Navigation : 

Fonctionnalités principales :
* Créer, gérer/ supprimer des tickets et des critiques
* S'abonner/ se désabonner à d'autres utilisateurs
* Consulter des feeds (tickets, critiques, utilisateurs)


## Principaux liens :
* Accueil : http://127.0.0.1:8000/home/
* Créer un ticket : http://127.0.0.1:8000/ticket/create/
* Créer une critique (sans ticket) : http://127.0.0.1:8000/review/create_with_ticket/
* Votre feed : http://127.0.0.1:8000/user_feed/
* Tickets en attente : http://127.0.0.1:8000/ticket_unchecked_feed/
* Utilisateurs suivis : http://127.0.0.1:8000/follow_users_page/

## Fonctionnement de l'application : 
Les modèles sont gérés dans review/models.py
Il existe 4 modèles : 
* User
* Ticket (lié à un user)
* Review (lié à un ticket et un user)
* UserFollows (lié deux users)

Ces objets (instances de modèles) sont traités au travers des formulaires suivants :
* LoginForm / SignupForm (pour l'User)
* ReviewForm
* TicketForm
* DeleteForm (pour ticket, critique et UserFollows)

Les vues sont gérées dans review/views.py
Il existe une view par page.
* Les feeds sont traités en ClassBasedView(CBV) (ListView)
* Les autres pages sont traitées en FunctionBasedView(FBV)

L'authentification des classes est gérée en héritant LoginRequiredMixin.\
Les fonctions possèdent le décorateur @login_required.

Il existe un template par type de page.\
Des snippets pour les tickets et critiques sont également présents pour l'affichage dans les feeds.


## Database :
La base de donnée est le fichier `db.sqlite3`.\
Les images sont stockées dans le dossier `media`.


## En savoir plus :
Les fonctions et méthodes sont documentées via docstrings avec leurs utilisations, arguments et retours.


## Générer un report flake8:
Installez flake8 html

* Commande terminal : `pip install flake8-html`

Lancez le report flake8 avec une longueur de ligne de 119 caractères.
* Commande terminal :`flake8 --max-line-length=119 --format=html --htmldir=flake-report`

Un nouveau dossier flake-report est créé, contenant index.html.
