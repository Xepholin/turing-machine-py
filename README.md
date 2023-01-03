# Machine de Turing
## En Python

Ce projet a été réalisé dans le cadre de l'UE Théorie des langages 2022-2023 et a pour but d'implémenter une simulation d'une machine de Turing en python.
Une documentation basique du code est disponible directement depuis le code source.

Le code de la MT doit être implémenté de la même manière que celui de https://turingmachinesimulator.com/, c'est à dire, il faut qu'il soit de la forme :

    name: nom
    init: nom_état_initial
    accept: nom_état_acceptant

    *le code de la MT*

Les commentaires ne sont pas autorisés dans le code.
Différents codes de MT sont disponibles dans MT_code.

### USAGE

    Calcul :
    python src/main.py calc <Entrée> <Chemin vers le code de la MT> 

    Linkage :
    python src/mains.py link <Entrée> <Chemin vers le code de la MT 1> <Chemin vers le code de la MT 2>

### Restriction sur la simulation

    Afin de ne pas avoir de problème lors du linkage, les appels de la 2ème MT devront être à la fin du code.

### En supplément

    L'aphabet d'entrée ainsi que l'alphabet de travail n'est n'est pas restraint par seulement [0, 1] et [0, 1, blank].

Ce projet a été développé par Marc Weng et Clément Richard en L3 Informatique TD4.