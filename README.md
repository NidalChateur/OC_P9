# LITReview : a Django application

The OCMovies-API project is a REST API application to be executed locally in the context
of educational projects. It provides movie information from GET http endpoints.
The API provides these endpoints to get detailed infomation about movies filtered by
various criteria such as genre, IMDB score or year. Endpoints allow users to retrieve
information for individual movies or lists of movies.

## Installation

This locally-executable API can be installed and executed from [http://localhost:8000/api/v1/titles/](http://localhost:8000/api/v1/titles/) using the following steps.


### Option 2: Installation and execution without pipenv (using venv and pip)

1. Clone this repository using `$ git clone clone https://github.com/OpenClassrooms-Student-Center/OCMovies-API-EN-FR.git` (you can also download the code using [as a zip file](https://github.com/OpenClassrooms-Student-Center/OCMovies-API-EN-FR/archive/refs/heads/master.zip))
2. Move to the ocmovies-api root folder with `$ cd ocmovies-api-en`
3. Create a virtual environment for the project with `$ py -m venv env` on windows or `$ python3 -m venv env` on macos or linux.
4. Activate the virtual environment with `$ env\Scripts\activate` on windows or `$ source env/bin/activate` on macos or linux.
5. Install project dependencies with `$ pip install -r requirements.txt`
6. Create and populate the project database with `$ python manage.py create_db`
7. Run the server with `$ python manage.py runserver`

When the server is running after step 7 of the procedure, the OCMovies API can be requested from endpoints starting with the following base URL: http://localhost:8000/api/v1/titles/.

Steps 1-3 and 5-6 are only required for initial installation. For subsequent launches of the API, you only have to execute steps 4 and 7 from the root folder of the project.


# LITReview : une application Django utilisant le framework Bootstrap v5.1

Notre nouvelle application permet de demander ou publier des critiques de livres ou d’articles. L’application présente trois cas d’utilisation principaux :

1. la publication des critiques de livres ou d’articles ;
2. la demande des critiques sur un livre ou sur un article particulier ;
3. la recherche d’articles et de livres intéressants à lire, en se basant sur les critiques des autres.

## Installation

Cette application Django exécutable localement peut être installée en suivant les étapes décrites ci-dessous. 

### Installation et exécution de l'application avec venv et pip

1. Cloner ce dépôt de code à l'aide de la commande `$ git clone clone https://github.com/NidalChateur/OC_P9_LITReview.git` (vous pouvez également télécharger le code [en temps qu'archive zip](https://github.com/NidalChateur/OC_P9_LITReview/archive/refs/heads/main.zip))
2. Rendez-vous depuis un terminal à la racine du répertoire OC_P9_LITReview avec la commande `$ cd OC_P9_LITReview`
3. Créer un environnement virtuel pour le projet avec `$ python -m venv env` sous windows ou `$ python3 -m venv env` sous macos ou linux.
4. Activez l'environnement virtuel avec `$ env\Scripts\activate` sous windows ou `$ source env/bin/activate` sous macos ou linux.
5. Installez les dépendances du projet avec la commande `$ pip install -r requirements.txt`
6. Démarrer le serveur avec `$ python manage.py runserver`

Lorsque le serveur fonctionne, après l'étape 6 de la procédure, l'application peut être consultée à partir de l'url [http://127.0.0.1:8000/].

Les étapes 1 à 6 ne sont requises que pout l'installation initiale. Pour les lancements ultérieurs du serveur de l'application, il suffit d'exécuter les étapes 4 et 6 à partir du répertoire racine du projet.
