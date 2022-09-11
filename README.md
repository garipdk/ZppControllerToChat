# ZppControllerToChat
Petit programme pour transformer des inputs de manette compatible XInput en texte dans le chat pour le [zeventplays Pokémon](https://www.twitch.tv/zeventplays).

Mettez votre curseur dans le chat du stream et lezgo ! Le programme entre votre commande avec une durée minimum de 1,5 secondes entre deux pour éviter de trop spam. 

Et faites des dons pour la planète ! Go vous renseigner sur https://zevent.fr !

# Utilisation
 - Touche A : tape "A" ou "a" dans le chat puis entrée
 - Touche B : tape "B" ou "b" dans le chat puis entrée
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

(Les majuscules et les minusculees sont alternées pour éviter les spam du même message)

# Comment l'exécuter ?
Go récupérer l'exécutable ici : https://github.com/rh0r/ZppControllerToChat/releases/tag/v1.2.1

Pour les utilisateurs de manettes DualSense, il faut passer par DS4Windows.

Si vous préférez exécuter le code il faut avoir python sur ton PC et exécuter le fichier main.py comme ça:

    py .\src\main.py

# Et pour faire un exécutable ?
Je fais ça avec pyinstaller:

    pyinstaller --onefile .\src\main.py
  
# Il est moche ton code
Ch'ui un dev C# et c'est littéralement mon premier programme en python, donc c'est normal si vous voyez des trucs pas ouf :-)

# Ca bug chez moi !
Hésitez pas à me contacter (Rhor#7868) sur le discord de Zerator !
