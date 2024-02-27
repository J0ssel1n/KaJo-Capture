<p align="center">
  <img src="https://github.com/J0ssel1n/KaJo-Capture/blob/main/Ressources/logo.png?raw=true" alt="drawing" width="500"/>
</p>

<p align="center">
  Un centre OpenLab. <a href="https://www.bing.com/images/create/une-petite-structure-bleue-au-premier-plan-qui-est/1-65c1f15c4c7c4131bcecc80955fe26ee?id=vvWNiAt7KLqr%2bBL0o6Wg2Q%3d%3d&view=detailv2&idpp=genimg&FORM=GCRIDP&mode=overlay">Voir le Prompt</a>.</p>

<h1 align="center">KaJo Capture</h1>
<p align="center">Un Projet de NSI par Josselin LE TALLEC et Kamal KANAAN.</p>

# Présentation
Incarnez un employé dévoué de l’organisation secrète OpenLab. Récemment, une expérience ratée a libéré les Jokas, des créatures dotées de pouvoirs extraordinaires, des laboratoires top secrets. Ces Jokas sont incontrôlables et menacent la sécurité de la population. 

_Votre mission est claire : les traquer, les capturer et les ramener en toute sécurité dans leur base de confinement._

Par les créateurs du célèbre **AlssExpress**, découvrez **Kajo Capture**, un jeu de combat au tour par tour où votre objectif est de capturer les Jokas en choisissant parmi ceux déjà capturés. Mais attention ! La difficulté augmente à mesure que vous passez d'une région à l'autre mais rassurez vous, vous aurez le choix d'améliorer votre équipement si cela vous enchante. Ce jeu est un **Die and Retry**, c'est-à-dire que si vous êtes amené à mourrir, vous perdrez votre progression et recommencerez depuis le début !

# Fonctionnement

Le jeu codé en Python utilise une base de données (**Database.db**) contenant des informations tels que les Jokas, la Carte, les Techniques utilisées par les Créatures, etc...

Google Colaboratory a été utilisé pour construire cette Base de Données (utile pour Tester et Afficher les Tables). Rendez-vous sur le <a href="https://colab.research.google.com/drive/1ZjbpvETwnX6evFEP1EMoqe3I823bBU86?usp=sharing">NoteBook</a> pour télécharger un fichier **Database.db** (Exécution > Tout exécuter > Attendre). Il faudra ensuite le Placer dans le Dossier Database et le Remplacer par le Précédent **Database.db**.

Le module SQLite3 a été utilisé pour Communiquer avec la Base de Données : Vous retrouverez Toutes les Fonctions utilisées pour Accéder aux Informations de la Base de Données dans <a href="https://github.com/J0ssel1n/KaJo-Capture/blob/main/Database/database.py">database.py</a>. Le module Tkinter a été utilisé pour la partie Graphique du Programme. Une version **Console** du Système de Combat est disponible dans <a href="https://github.com/J0ssel1n/KaJo-Capture/blob/main/Combat/game.py">game.py</a>.

# Installation

**Le Programme n'est pas encore Disponible** et est toujours en Phase de Test. Il reste des Bugs à régler (notamment celui où le Joka Principal n'en fait qu'à sa tête en Combat dans <a href="https://github.com/J0ssel1n/KaJo-Capture/blob/main/main.py">main.py</a>. Vous pourrez retrouvez un exécutable en _.exe_ créé avec PyInstaller dans <a href="https://github.com/J0ssel1n/KaJo-Capture/releases">Releases</a>.

# Rapport de Projet

Le Rapport est en Cours de Rédaction.

# Informations

Ce Projet utilise la licence MIT qui permet aux Utilisateurs de faire ce qu'ils veulent avec le Code tant qu'ils incluent la Notice de Copyright et la Clause de Non-Responsabilité.

Ce Texte a été rédigé en Markdown pour Présenter le Projet sur GitHub. Merci de votre Lecture.
