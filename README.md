# bot_cote_boost-e_winamax

Un partage de code et une stratégie exhaustive afin de prendre automatiquement toutes les grosses cotes boostées winamax. 

Grâce à des outils comme Selenium, des API Telegram, des proxys résidentiels et des VM, ce README explique en détail comment créer un bot parfaitement indétectable par winamax.

Dans ce projet, vous aurez besoin d'une Raspberry Pi, et d'être familier avec certaines notions de librairies Python comme Selenium, mais aussi des notions de paris sportifs comme l'arbitrage.

## Voici les grandes lignes du projet :

1. Setup une machine virtuelle (plus complexe) ou une Raspberry pour laisser tourner le futur bot.
2. Créer un système d'alerte lors de la sortie d'une cote boostée chez winamax et en extraire l'intitulé
3. Construire un driver automatisé indétectable par winamax avec Selenium.
4. Mettre en place un processus de prise de cote automatisé avec l'information du pari à prendre.
5. Orchestrer le tout en un code multithreading tournant constamment, capable de reboot et avec des débugs.

---

/!\ TOUT LES CODES SONT FOURNIS DANS LES DOSSIERS CORRESPONDANTS, POUR CHAQUE ETAPE DU PROJET /!\

---

### 1. Setup une Raspberry

Une Raspberry, c'est un peu comme un ordinateur, sauf qu'il n'y a pas de périphériques : pas d'écrans, pas de souris, pas de clavier, etc. 

Ça tombe bien car ce n'est pas cher et ça va nous permettre de laisser tourner notre bot afin qu'il prenne toutes les grosses cotes boostées par lui-même. Vous pouvez en trouver sur leboncoin pour 40/50 euros avec le câble d'alimentation puis l'installer chez vous. Une fois connectée en SSH sur la Raspberry (des milliards de tutos existent), veillez à bien créer un environnement virtuel et installer les librairies suivantes en Python :

### 2. Créer un système d'alerte de cote sortie

Pour créer un système capable d'alerter notre bot qu'une grosse cote boostée vient de sortir, il y a plusieurs options : j'avais essayé d'extraire les tweets récents en boucle de @alerte_gcb sur Twitter, mais ce n'était pas assez fiable.

Je me suis donc penché sur un bot annexe Telegram, provenant toujours du propriétaire du compte @alerte_gcb (énorme respect pour la qualité de son travail d'ailleurs). J'ai donc initialement créé un script qui vérifie les messages de ce bot annexe.

La solution : créer une application Telegram, et avec la librairie Python associée, extraire chaque message reçu par le créateur de l'application. Je conseille de vous créer un compte Telegram à cet effet.

### 3. Construire un driver indétectable avec Selenium

Les bonnes vieilles techniques de scraping classique avec Selenium, comme changer le user agent ou implémenter un délai aléatoire entre chaque action du bot sur la page web, ne marchent pas sur winamax.

De plus, le mode headless de Selenium est facile à détecter pour les systèmes anti-bot de winamax. Il a été donc très difficile de trouver une combinaison de paramètres du driver capable de passer inaperçue.

En effet, pendant un certain temps, j'arrivais à me connecter avec le driver sans mode headless, mais dès que je l'activais, j'avais un message d'erreur sur l'authentification. Heureusement, j'ai trouvé des settings du driver qui fonctionnent.

### 4. Le code multithreading

Rien de plus simple, récapitulons ce que fait le bot jusqu'à présent. En compilant le main code, le thread principal de message handler attend que le créateur de l'application Telegram (vous) reçoive une alerte de cote boostée.

Cette fonction va sur le site winamax.fr, accepte les cookies, se connecte (votre login et mot de passe), met votre date de naissance, se dirige vers la page des cotes boostées, sélectionne celle dont vous avez été alerté, et place le pari automatiquement.

Des débugs ont été ajoutés. L'étape la plus difficile consiste en fait à passer l'authentification automatique : si votre driver est mal configuré, winamax vous renverra un message de problèmes d'authentification.


---

NOTES IMPORTANTES : veillez à ce que les requêtes web du bot se fassent sous votre adresse ip publique, c'est à dire que la raspberry soit connectée à votre wifi personnel, autrement votre compte winamax se fera bannir sur le long terme. 
Pour surmonter ce problème d'ip, la piste des proxys résidentiels rotatifs était à première vue une bonne solution : mais selenium a du mal à combiner les présets complexes d'un driver indétectable + des options de proxys.
On aurait pu penser aussi à l'utilisation de vpn privés sur la raspberry (pour le prix de quelques euros par mois en plus d'un abonnement classique, on peut en avoir une ip dédiée et sécurisée), piste à explorer...

---
