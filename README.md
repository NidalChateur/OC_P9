# LITReview : A Django application using the Bootstrap framework v5.1.


Our new application allows users to request or publish reviews of books or articles. The application features three main use cases:

1. Publishing reviews of books or articles.
2. Requesting reviews on a specific book or article.
3. Searching for interesting articles and books to read, based on others' reviews.

## Installation

This locally executable Django application can be installed by following the steps outlined below. If you haven't installed Python on your PC yet, you can download it via this link: https://www.python.org/downloads/ and then install it.


### Installation and Execution of the Application using venv and pip

1. Clone this repository using `$ git clone clone https://github.com/NidalChateur/OC_P9_LITReview.git` (you can also download the code using [as a zip file](https://github.com/NidalChateur/OC_P9_LITReview/archive/refs/heads/main.zip))
2. Move to the OC_P9_LITReview root folder with `$ cd OC_P9_LITReview`
3. Create a virtual environment for the project with `$ py -m venv env` on windows or `$ python3 -m venv env` on macos or linux.
4. Activate the virtual environment with `$ env\Scripts\activate` on windows or `$ source env/bin/activate` on macos or linux.
5. Install project dependencies with `$ pip install -r requirements.txt`
6. Run the server with `$ python manage.py runserver`

When the server is running, after step 6 of the procedure, the application can be accessed from the URL : http://localhost:8000/api/v1/titles/.

Steps 1 to 6 are only required for the initial installation. For subsequent launches of the application server, simply execute steps 4 and 6 from the project's root directory.


# LITReview : une application Django utilisant le framework Bootstrap v5.1

Notre nouvelle application permet de demander ou publier des critiques de livres ou d’articles. L’application présente trois cas d’utilisation principaux :

1. la publication des critiques de livres ou d’articles ;
2. la demande des critiques sur un livre ou sur un article particulier ;
3. la recherche d’articles et de livres intéressants à lire, en se basant sur les critiques des autres.

## Installation

Cette application Django exécutable localement peut être installée en suivant les étapes décrites ci-dessous. Si vous n'avez pas encore installé Python sur votre PC, vous pouvez le télécharger via ce lien : https://www.python.org/downloads/ puis l'installer.

### Installation et exécution de l'application avec venv et pip

1. Cloner ce dépôt de code à l'aide de la commande `$ git clone clone https://github.com/NidalChateur/OC_P9_LITReview.git` (vous pouvez également télécharger le code [en temps qu'archive zip](https://github.com/NidalChateur/OC_P9_LITReview/archive/refs/heads/main.zip))
2. Rendez-vous depuis un terminal à la racine du répertoire OC_P9_LITReview avec la commande `$ cd OC_P9_LITReview`
3. Créer un environnement virtuel pour le projet avec `$ python -m venv env` sous windows ou `$ python3 -m venv env` sous macos ou linux.
4. Activez l'environnement virtuel avec `$ env\Scripts\activate` sous windows ou `$ source env/bin/activate` sous macos ou linux.
5. Installez les dépendances du projet avec la commande `$ pip install -r requirements.txt`
6. Démarrer le serveur avec `$ python manage.py runserver`

Lorsque le serveur fonctionne, après l'étape 6 de la procédure, l'application peut être consultée à partir de l'url [http://127.0.0.1:8000/].

Les étapes 1 à 6 ne sont requises que pout l'installation initiale. Pour les lancements ultérieurs du serveur de l'application, il suffit d'exécuter les étapes 4 et 6 à partir du répertoire racine du projet.
