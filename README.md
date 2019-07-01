# Melia
Algorithme de détection de mouvement basé sur une prise en rafale de photos

L'objectif ici et d'utiliser Python et la librairie Opencv afin de realiser une détection de mouvement. Pour cela, on se base sur une série de photos prises en rafale et on effectue une comparaison entre deux images. Un mouvement a été simulé en bougeant une figurine entre deux cliché successifs.

Remarque : on ne fait pas de la détection profil ou de forme ici, on compare juste la différence entre deux images.

Les résultats sont les suivants :

![Original](http://thibault.giauffret.free.fr/git/images/melia/original.png)
![Modified](http://thibault.giauffret.free.fr/git/images/melia/modified.png)
![Diff](http://thibault.giauffret.free.fr/git/images/melia/diff.png)

 À termes, ce script se révèle intéressant pour traiter un grand nombre de donnée s(comme par exemple un ensemble de photos prises par une camera de sécurité avec détection infrarouge). Sur un grand nombre de clichés, le script permet de ne garder que ceux résultant du mouvement d'une personne ou d'un véhicule.

Deux versions sont proposées :
- Melia Console : une version console uniquement qui une fois configurée n'a plus qu'à être exécuté ;
- Melia GUI : une version GUI qui permet l'affichage des zones où le mouvement est détecté.

Dans tous les cas, il sera nécessaire d'installer Python 3.7 et de charger les librairies suivantes :
- scikit-image
- imutils
- opencv-python
- shutil
- glob
- os
- datetime

Remarque : si elle ne sont pas installées par défaut, les charger avec un utilitaire de librairie tel que <em>pip</em>.

Le détail du fonctionnement du script est donné dans les fichiers <em>py</em>.
