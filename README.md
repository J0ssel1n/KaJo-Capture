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

https://doc-08-30-docstext.googleusercontent.com/export/m1s28lvl796g4kelob4lsl26u4/91p2eg8nv6pg9odinmhoc92v6s/1709163935000/110151984853555692055/110151984853555692055/1PPtIGIhl3rV-qv2M0MYLZZXl8kC6M5oYJkS7IeXytL0?format=pdf&id=1PPtIGIhl3rV-qv2M0MYLZZXl8kC6M5oYJkS7IeXytL0&token=AC4w5VjwgXcMTEUHsDxbUtby2o6GQegiSw:1709161982787&ouid=110151984853555692055&includes_info_params=true&usp=drive_web&cros_files=false&inspectorResult=%7B%22pc%22:3,%22lplc%22:16%7D&dat=AOBvIb2GW8N14EKlxGTIndM7CXQFFfMLqxQ5ZI495_9JQAIEhKBKMpX9F9F9clnh5IT0UA2P657tIz5AqBkvyURM0QLsIhwJ1oPQoeNjtXlwzQIO_HgoU_yBf0vS5ccPIX9l2Pfb33xX0lHpfa__JMcpTep4Kr5ZCdlhJ77TSffFXmyk3ymjMUI2W63ONUj0DoJbxuXYcD00WGn930Sk6S8KXDOTjLaOSfsrj-nDX2-G7HUlrJXcYNKL12CTrSDa9GY3Ves29jQdB0iEfAW05Cfz1ZHTHl2QXsn_yI6tGZgZz-h3A0-OQrWjA0Enjd1RUTZwJ83CTVVLYLLdJdiZhQtOcytIoyqLMKdPjmbbbV9oAPYSHEr6LzhSwBY32mX-WkAWjp6oBCva5TFkpZDq9WxdUVQf0OjFbk1DKVt9JqQdSw_GMwg-KmHjNwKKym54V7ZsZ4Tqu7pCQg-A_RMGzGIoR3s_jXNu9H1gnFlVyzoHs9SQcwGM_J8VvQ2I9Q6ZsNG5fijFLGgszMp3hucCKGkzlqwFUQdnuYC0DeJi-iuPeLvoR1i61a91V552HtjdBQQ8wMwZw5pzjkrYrDlw4NJ498BoiGONUrdlKIihFugND1AZMcZH5M166Wx0w6L-thBsBW_wwVcmnc-ZYinn8CsemGMPN1JhW1dbKjEOARKVrzJxrCI6EA1hUssHxhi0v3SXg6AY6hpy0HNvKdoWnedyS37hrZtqWy-47YzwyixcPCGtrGpn5XGe7VOpiNU9-pnRkjL9Qcn5L63lDPEFhDuPjIj0v6qHy7R60wHNnc52g3fYy4R8RhdTIilzwYh3RG8VBIkFBAxIC22gZMgmC5_sK7dPHohr29sPSYgTO9Cxankympnh5KUr16ONXIWkSiVdNJxfiwXtUn_gNDlWPesQoVcewuTcoVbGL6C02-waKWWMbAuJEpKhnobA

# Informations

Ce Projet utilise la licence MIT qui permet aux Utilisateurs de faire ce qu'ils veulent avec le Code tant qu'ils incluent la Notice de Copyright et la Clause de Non-Responsabilité.

Ce Texte a été rédigé en Markdown pour Présenter le Projet sur GitHub. Merci de votre Lecture.
