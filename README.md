# ZppControllerToChat
Assez gros programme pour transformer des inputs d'à peut près toutes les manettes (XBox/PS(4/5)/Switch) en texte dans le chat pour le zeventplays Pokémon : https://www.twitch.tv/zeventplays.

(Si t'as une manette hyper funky qui est ni une thrustmaster ni une ultimate (celle ci sont supportées également) que je ne connais pas contacte moi (GapirAte) sur le discord de Zerator)

Met ton curseur dans le chat du stream et lezgo ! Le programme entre ta commande avec une durée minimum de 1,5 secondes entre deux pour éviter de trop spam. 

Et fait des dons pour les gens en dificulté en france ! Go te renseigner sur https://zevent.fr !

GG d'avance à tous pour les X XXX XXX€ !!!

# D'où viens le visu des manettes xbox1 et ps4 ?
D'ici : https://github.com/Sitryk/gamepadviewer-python
J'ai lu le code et il est clean d'après moi donc je l'ai intégré à ce projet et je le cite ici pour pas avoir de problèmes
Normalement avec ça license il devrait pas y avoir de soucis mais si il y en a contacte moi en réagissant sur ce projet

# Utilisation
 - Touche A : tape "A" ou "a" dans le chat puis entrée
 - Touche B : tape "B" ou "b" dans le chat puis entrée
 - Touche X : tape "X" ou "x" dans le chat puis entrée (Il y aura deux version selon si les touches X et Y sont présents ou non dans le jeu)
 - Touche Y : tape "Y" ou "y" dans le chat puis entrée (Il y aura deux version selon si les touches X et Y sont présents ou non dans le jeu)
 - Touche haut ou un joystick vers le haut : tape "HAUT" ou "haut" dans
   le chat puis entrée
 - Touche bas ou un joystick vers le bas : tape "BAS" ou "bas" dans le
   chat puis entrée
 - Touche gauche ou un joystick vers la gauche : tape "GAUCHE" ou
   "gauche" dans le chat puis entrée
 - Touche droite ou un joystick vers la droite : tape "DROITE" ou
   "droite" dans le chat puis entrée
 - Touche gachette droite du haut : colle ce qui a été copié puis entrée
 - Appuyer sur le joystick gauche : quitte l'application
 - Touche START : tape "START" ou "start" dans le chat puis entrée

(Les majuscules et les minusculees sont alternées pour éviter les spam du même message)

# Comment l'exécuter ?
Go récupérer l'exécutable ici : https://github.com/garipdk/ZppControllerToChat/releases

Si tu préfére exécuter le code toi même exécute il faut avoir python avec toutes les dépendances installées sur ton PC et exécuter le fichier zppControllerToChatV2_withKeysXY.py comme ça:

    py .\src\zppControllerToChatV2_withKeysXY.py
    ou
    python3 .\src\zppControllerToChatV2_withKeysXY.py
    ou
    py .\src\zppControllerToChatV2_withoutKeysXY.py
    ou
    python3 .\src\zppControllerToChatV2_withoutKeysXY.py

# Et pour faire un exécutable ?
Je fais ça avec pyinstaller:

    pyinstaller --icon=JJJJJ.ico --onefile .\src\zppControllerToChatV2_withKeysXY.py .\src\assets.py --add-data .\src\main_assets:main_assets
    ou
    pyinstaller --icon=JJJJJ.ico --onefile .\src\zppControllerToChatV2_withoutKeysXY.py .\src\assets.py --add-data .\src\main_assets:main_assets
    ou
    pyinstaller --icon=JJJJJ.ico --onefile .\src\zppControllerToChatV2Light_withKeysXY.py
    ou
    pyinstaller --icon=JJJJJ.ico --onefile .\src\zppControllerToChatV2Light_withoutKeysXY.py
  
# Il est moche ton code
Ch'ui un dev C++ à la base mais c'est pas mon premier programme en python, donc j'espère que c'est pas si moche quant même ^^

# Ca bug chez moi !
Hésite pas à me contacter (GapirAte) sur le discord de Zerator !

# Comment je fais pour que windows ne détecte pas les exe comme des virus ?
Je créé un ticket par exe dans ce scanner de windows : https://www.microsoft.com/en-us/wdsi/filesubmission
Mais ça peut prendre 6h en version légère et plus de 10h en version lourde pour que le scanner décrète que ce n'est pas un virus
Il est possible d'acheter une acréditation pour que ça aille plus vite mais pour l'instant flemme
