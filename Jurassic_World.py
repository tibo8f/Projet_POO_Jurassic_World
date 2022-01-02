"""
Projet jurrasic world
Cours de programation orienté objet

François Thibaut 195195
Hermans Jordan
"""

import random
from random import randint
import copy
import math
import pygame
import time



class World:
    """
    La classe world met en place le monde et gère toutes les interactions avec le monde. 
    Par exemple la transformation d'un item en un autre quand il meurt, l'interface graphique du monde.
    """
    def __init__(self):
        """
        Cette fonction associe au nouvel objet world un plateau rempli avec les items d'iniitialisation que l'on peut choisir.
        Elle commence par créer un plateau vide selon les dimenssions voulues. Puis elle ajoute les items selon le nombre choisi
        sur le plateau. Des paramètres initiaux sont proposés pour ne pas devoir tout encoder à chaque fois qu'on lance le jeu.
        """

        # CREATION D'UN PLATEAU VIDE

        
        self.nbline = 10
        self.nbcolumn = 10

        self.nbcases = self.nbline*self.nbcolumn
        self.empty_case = '--'
        self.board = [[self.empty_case for i in range(self.nbcolumn)] for j in range(self.nbline)]      
        self.round_number = 1

        # AJOUT DES ITEMS DE BASE
        
        print("Voulez vous choisir les paramètre? taper 1 pour choisir, taper 2 pour les paramètres par défaut")
        self.parametre = int(input())

        number_of_item_max = self.nbcases // 10        # mise en place d'un maximum de 10% du plateau pour chaque items
        if number_of_item_max <1:                     # mise en place d'un minimum d'une unité si plateau petit
            number_of_item_max = 1

        list_of_name = ["Tyrannosaure", "Stegosaure", "Brachiosaure", "Velociraptor", "Rose", "Bush", "Trees"]      # les différents items
        initial_types_items = [Tyrannosaure, Stegosaure, Brachiosaure, Velociraptor, Rose, Bush, Trees]

        # boucle qui demande le nombre de chaque item et qui l'ajoute dans le plateau
        for i in range(len(list_of_name)):
            type_of_object = initial_types_items[i]
            if self.parametre == 2:
                nbitem = 6
            else:
                print("inséré le nombre de ", list_of_name[i] ,". Le maximum est de ", number_of_item_max)
                nbitem = int(input())
                while nbitem > number_of_item_max or nbitem < 0:
                    print("le nombre de ", list_of_name[i], "doit être un entier compris entre 0 et ", number_of_item_max)
                    nbitem = int(input())

            # ajout des items dans le plateau
            for j in range(nbitem):
                ligne = randint(0, self.nbline -1)
                colonne = randint(0, self.nbcolumn -1)
                no_infinite_boucle = 50                                     # empecher les boucles infinies
                while self.board[ligne][colonne] != self.empty_case:        # vérifie que la case est vide
                    ligne = randint(0, self.nbline -1)
                    colonne = randint(0, self.nbcolumn -1)
                    no_infinite_boucle -= 1
                    if no_infinite_boucle <0:
                        print("erreur boucle infinie dans la fonction items on board")
                        print("le plateau n'est pas assez grand pour ajouter cet item")
                        break
                
                new_object = type_of_object(ligne, colonne) 
                self.board[ligne][colonne] = new_object



    def affichage_plateau(self):
        """
        Cette fonction s'occupait d'afficher le plateau dans le terminal avant d'être remplacé par une interface graphique pygame

        Entrées : instances de la classe World
        Sorties : /
        """
        display = copy.deepcopy(self.board)         # deepcopy nécessaire sinon on modifie self.board en meme temps que display
        line_index = 0
        for line in display:
            column_index = 0
            for case in line:
                if type(case) != type(self.empty_case):
                    display[line_index][column_index] = case.symbol
                column_index += 1
            line_index += 1

        print("plateau de jeu :")
        for line in display :
            print(line)
        
        

    def get_board(self):
        """
        Cette fonction permet aux autre fonctions des autres classes de récupérer le plateau de jeu. Cela leur permettra de communiquer avec
        les autres items du jeu.

        Entrées : instances de la classe World
        Sorties : une la plateau de jeu sous forme d'une matrice
        """
        return self.board



    def round(self):
        """
        Cette fonction s'occuppe de faire vivre le jeu à chaque tour.
        Elle est appellée chaque tour et elle appelle les fonctions du jeu sur les objets, comme perdre des vies, mourir, ...
        Les fonctions appellées sur les objets sont appellée dans l'ordre de priorité.
        Il est nécessaire de regarder si l'item a déjà  joué avant d'appeller une autre fonction pour qu'un item ne joue pas 
        2 fois d'affilé.

        Entrées : instances de la classe World
        Sorties : /
        """
        for line in self.board:
            for item in line:         
                if isinstance(item, LifeForm) and item.already_played == "NO":
                    item.energy_loss()
                    item.health_loss()
                    item.dye(item)
                    if item.already_played == "NO":
                        item.feed()                         
                    if item.already_played == "NO":
                        item.reproduction()         # a mettre au dessus pour vérifié que les animaux ne sont pas en gestation avant de leurs demander de faire autre chose
                
                    if isinstance(item, Carnivore) and item.already_played == "NO":
                        item.attack()

                    if isinstance(item, Animal) and item.already_played == "NO":
                        item.poop()
                        if item.already_played == "NO":
                            item.move()             # doit être placée en dernier car si l'animal ne sait rien faire il bougera

                if isinstance(item, Meat):
                    item.dye()
                                                                              
        # en fin de round il faut reset le fait que les formes de vies ont déja joué et 
        # changer l'état des déchets et viandes qui sont mtn disponible à etre mangé au tour suivant
        for line in self.board:
            for item in line:
                if isinstance(item, OrganicWaste) or isinstance(item, Plant) or isinstance(item, Meat):
                    item.waitaround = "YES"
                if isinstance(item, LifeForm):
                    item.already_played = "NO"
                    item.round_alive += 1
                if isinstance(item, Meat):
                    item.round_alive += 1

        self.round_number += 1



    def change_item(self, item, line, column):
        """
        Cette fonction remplace un item par un autre sur le plateau
        
        Entrée : instances de la classe World, le nouvel item à changer, la ligne et la colonne de l'item à changer
        Sorties : /
        """
        self.board[line][column] = item



    def remove_item(self, line, column):
        """
        Cette fonction retire un item du plateau de jeu

        Entrée : instances de la classe World, la ligne et la colonne de l'item à enlever
        Sorties : /
        """
        self.board[line][column] = self.empty_case



    def add_item(self, item, line, column):
        """
        Cette fonction ajoute un nouvel item sur le plateau

        Entrée : instances de la classe World, le nouvel item, la ligne et la colonne du nouvel item
        Sorties : /
        """
        self.board[line][column] = item



    def move_item(self, item, old_line, old_column, new_line,new_column):
        """
        Cette fonction déplace un item (les animaux) sur le plateau.

        Entrée : instances de la classe World, l'item à déplacer, l'ancienne ligne et l'ancienne colonne de l'item,
                 la nouvelle ligne et la nouvelle colonne de l'item
        Sorties : /            
        """
        self.board[old_line][old_column] = self.empty_case
        self.board[new_line][new_column] = item

    



        




class Item:
    """
    La classe Item est la classe mère de tous les objets sur le plateau.
    Les items sont les objets sur le plateau.

    Classe mère : /
    Classe fille : LifeForm, Meat, OraganicWaste
    """
    def __init__(self, line, column):
        """
        Chaque objet possède une ligne et une colonne et un compteur du nombre de tour qu'il a passé sur le plateau.

        Entrée : la ligne et la colonne de l'item
        Sorties : /
        """
        self.line = line
        self.column = column
        self.round_alive = 1
        


    






class LifeForm(Item):
    """
    La classe LifeForm reprend les points commun de toutes les formes de vies
    Les formes de vies perdent des vies et de l'énergie au fur et à mesure du temps. Les formes de vies
    meurent aussi mais elles meurent toutes d'une façon différente donc les méthodes dye ont été définies dans 
    les classes filles.

    Classe mère : Item
    Classe fille : Plant et Animal
    """
    def __init__(self, line, column):
        """
        Chaques forme de vie a les instances de la classe item.
        En plus de ces instances une formes de vie a de nouvelles instances : des points de vies, des points d'énergie
        et une indication sur le fait qu'elle ait déjà jouée.

        Entrées : instances de la classe LifeForm, la ligne et la colonne de la forme de vie
        Sorties : /
        """
        Item.__init__(self, line, column)
        self.health = 10
        self.energy = 10
        self.already_played = "NO"
        self.vision = 3



    def energy_loss(self):
        """
        Cette fonction fait perdre un point d'énergie a toutes les formes de vies (chaque tour).

        Entrées : instances de la classe LifeForm
        Sorties : /
        """
        if self.energy > 0 :
            self.energy-=1



    def health_loss(self):
        """
        Cette foonction fait perdre un point de vie par tour à toutes les formes de vies qui n'ont plus d'énergie.

        Entrée : instances de la classe LifeForm
        Sorties : /
        """
        if self.energy == 0 and self.health > 0:
            self.health -= 1










class Meat(Item):
    """
    La classe Meat reprends les méthodes des animaux morts

    Classe mère : Item
    Classe fille : /
    """
    def __init__(self, line, column):
        """
        Chaque viande a les instances de la classe Item plus les nouvelles instances de la classe Meat :
        un symbol qui sera utile pour l'affichage dans le terminal et une indication sur l'attente d'un tour qui sert 
        a laisser la viande affiché un tour avant que les carnivores puissent la manger.

        Entrées : instances de la classe Meat, la ligne et la colonne de la viande
        Sorties : /
        """
        Item.__init__(self, line, column)
        self.symbol = "Me"
        self.waitaround = "NO"
        self.image = pygame.image.load('assets/meat.png')



    def dye(self):
        """
        Cette fonction transforme la viande en déchet organique après un certain temps.

        Entrées : instances de la classe Meat
        Sorties : /
        """
        if self.round_alive > 10:                           # après 10 tours la viande se tranforme en déchet organique
            waste = OrganicWaste(self.line, self.column)
            world.change_item(waste, self.line, self.column)
            print("la viande à la case", self.line, self.column, "a péri et est devenu un déchet organique")










class OrganicWaste(Item):
    """
    La classe OrganicWaste reprend les méthodes des déchets organiques.

    Classe mère : Item
    Classe fille : /
    """
    def __init__(self, line, column):
        """
        Les déchets organiques ont les instances de la classe Item plus les nouvelles instances de la classe OrganicWaste:
        un symbol qui sera utile pour l'affichage dans le terminal et une indication sur l'attente d'un tour qui sert 
        a laisser le déchet organique affiché un tour avant que les plantes puissent le manger.

        Entrées : instances de la classe OrganicWaste, la ligne et la colonne du déchet organique
        Sorties : /
        """
        Item.__init__(self, line, column)
        self.symbol = "Ow"
        self.waitaround = "NO"
        self.image = pygame.image.load('assets/organicWaste.png')










class Plant(LifeForm):
    """
    La classe Plant reprend les méthodes des plantes. Les plantes sont des formes de vies et donc des items.
    Les plantes peuvent se nourir et se reproduire.

    Classe mère : LifeForm
    Classes filles : Trees, Bush, Rose
    """
    def __init__(self, line, column):
        """
        Les Plantes ont les instances de la classe LifeForm plus une nouvelle instances de la classe Plant qui 
        indique si la plante a attendu un tour avant de pouvoir rejouer.

        Entrées : instances de la classe Plant, la ligne et la colonne de la plante
        Sorties : /
        """
        LifeForm.__init__(self, line, column)
        self.waitaround = "NO"
        self.semis_zone = 2
        self.racines_zone = 3



    def dye(self, name):
        """
        Cette fonction fait mourir les plantes si elles n'ont plus de points de vies. Une plante se transforme
        en déchet organique lorsqu'elle meurt.

        Entrées : instances de la classe Plant, le nom de l'objet de type plante
        Sorties : /
        """
        if self.health == 0:
            print("la plante", name,"à la case",self.line,self.column,"meurt")
            waste = OrganicWaste(self.line, self.column)
            world.change_item(waste, self.line, self.column)
            world.board
            self.already_played = "YES"



    def feed(self):
        """
        Cette fonction s'occuppe de l'alimentation des plantes : elles se nourissent de déchets organique.
        Les déchets organiques doivent se trouver dans la zonede racine de la plante pour qu'elle puisse
        le manger.

        Entrées : instances de la classe Plant
        Sorties : /
        """
        board = world.get_board()
        vision = Zone(board, self.line, self.column)
        feed_zone = vision.vision_en_cercle(self.racines_zone)
        cases_with_organic_waste = []
        for case in feed_zone:
            if isinstance(board[case[0]][case[1]], OrganicWaste):
                if board[case[0]][case[1]].waitaround=="YES":          # check supplémentaire sur la plante a déjà joué 
                    cases_with_organic_waste += [case]
        
        if cases_with_organic_waste != []:
            case = random.choice(cases_with_organic_waste)
            self.health += 1
            self.energy += 10
            world.remove_item(case[0],case[1])
            print("la plante a la ligne", self.line, self.column, "a mangé le déchet organique à la case", case)
            self.already_played = "YES"



    def reproduction(self):
        """
        Cette fonction s'occuppe de la  reproduction des plantes. Elles se reproduisent dans la zone de semis.

        Entrées : instances de la classe Plant
        Sorties : /
        """
        board = world.get_board()
        vision = Zone(board, self.line, self.column)
        reproduction_zone = vision.vision_en_cercle(self.semis_zone)
        type_item = [Rose, Bush, Trees]

        cases = []
        if self.round_alive%5 == 0:         # une plante se reproduit tous les 5 tours (changer le modulo pour changer le nombre de tours)
            for case in reproduction_zone:
                if type(board[case[0]][case[1]]) == type('--'):
                    cases += [case]
        
        if cases != []:
            case_chosen = random.choice(cases)
            for i in type_item:
                if isinstance(board[self.line][self.column], i):
                    new_item = i(case_chosen[0], case_chosen[1])
                    print("une nouvelle plante est créée", new_item, "à la case", case_chosen[0], case_chosen[1])
                    world.add_item(new_item, case_chosen[0], case_chosen[1])
                    self.already_played = "YES"










class Animal(LifeForm):
    """
    La classe Animal reprend les méthodes des animaux. Les animaux sont des sortes de vie et sont donc des items.
    Les animaux peuvent se déplacer, se reproduire et faire caca.

    Classe mère : LifeForm
    Classes filles : Carnivores, Herbivores
    """
    def __init__(self, line, column):
        """
        Les Animaux ont les instances de la classe LifeForm plus de nouvelles instances de la classe Animal :
        Une instance indiquant le sexe de l'animal, une instance indiquant si l'animal est en gestation et 
        une instance indiquand depuis combien de tour l'animal est en gestation (0 si il n'est pas en gestation).

        Entrées : instances de la classe Animal, la ligne et la colonne de l'animal
        Sorties : /
        """
        LifeForm.__init__(self, line, column)
        self.genre = random.choice(["F","M"])
        self.gestation = "NO"                         
        self.round_in_gestation = 0



    def dye(self, name):
        """
        La fonction dye fait mourir les animaux si ils n'ont plus de points de vies. Un animal se transforme en 
        viande lorsqu'il meurt.

        Entrées : instances de la classe Animal, nom de l'objet animal.
        Sorties : /
        """
        if self.health <= 0:
            print("le ", name," meurt")
            meat = Meat(self.line, self.column)
            world.change_item(meat, self.line, self.column)
            self.already_played = "YES"



    def reproduction(self):
        """
        La fonction reproduction s'occupe de la reproduction entre les animaux.
        La reproduction se déroule en 3 fases:
            période de golo golo : 2 animaux de la même espèce et de sexe différent peuvent se reproduirent
                dans la zone de contact 
            période de gestations : les 2 animaux ne peuvent plus bouger pendant un certain nombre de tours
            accouchement : un bébé nait a côté de la femmelle 
        Cette fonction s'occuppe des 3 phases.
        
        Entrées : instances de la classe Animal.
        Sorties : /
        """
        board = world.get_board()
        my_animal = board[self.line][self.column]
        if isinstance(my_animal, Animal):                   # antibug devient une viande et puis la fonction reproduction est appellée
            zone = Zone(board, self.line, self.column)
            contact_zone = zone.contact_zone()
            type_item = [Tyrannosaure, Stegosaure, Brachiosaure, Velociraptor]
            cases = []
        

            # PHASE D'ACCOUCHEMENT

            if my_animal.gestation =="YES":
                self.already_played = "YES"
                if self.round_in_gestation >10:         # 10 tours de gestations avant l'accouchement    
                    if my_animal.genre == "F":
                        for case in contact_zone:
                            if type(board[case[0]][case[1]]) == type("--"):
                                cases += [case]
                        
                        if cases !=[]:
                            case = random.choice(cases)         
                            for i in type_item:                  
                                if isinstance(board[self.line][self.column], i):
                                    new_item = i(case[0], case[1])    

                            print("un nouvel animal est né", new_item, "à la case", case[0], case[1])
                            world.add_item(new_item, case[0], case[1])
             
                        else:
                            print("la mère à la case", self.line, self.column, "n'a pas pu accoucher de son bebe car il n'y avait plus de place autour")     

                    self.round_in_gestation = 0
                    self.gestation = "NO"


            # PHASE DE GESTATION

                else:
                    self.round_in_gestation += 1
                    print("L'animal", my_animal, "à la case", self.line, self.column, "est en gestation")


            # PHASE DE GOLO GOLO

            else:
                for case in contact_zone:
                    item =board[case[0]][case[1]]
                    if isinstance(item, type(my_animal)) and item.genre != my_animal.genre and my_animal.round_in_gestation == 0:
                        item.gestation = "YES"
                        my_animal.gestation = "YES"
                        print("les animaux", my_animal, "et", item, "aux cases", self.line, self.column, "et", item.line, item.column, "se mettent en gestation d'une durée de 10 tours (ils ne doivent plus bouger)")
                        self.already_played = "YES"



    def poop(self):
        """
        Cette fonction s'occupe de la digestion des animaux : les animaux laissent régulièrement des déchets organiques derrière eux.
        
        Entrées : instances de la classe Animal.
        Sorties : /
        """
        board = world.get_board()
        zone = Zone(board, self.line, self.column)
        contact_zone = zone.contact_zone()
        cases = []
        if self.round_alive%10 == 0:                 # tous les 10 tours les animaux font cacas
            for case in contact_zone:
                item = board[case[0]][case[1]]
                if type(item) == type("--"):
                    cases += [case]
            if cases != []:
                case = random.choice(cases)
                line = case[0]
                column = case[1]
                waste = OrganicWaste(line, column)
                world.add_item(waste, line, column)
                print("l'animal", board[self.line][self.column], "à fait caca à la case", line, column)
                self.already_played = "YES"










class Carnivore(Animal):
    """
    La classe Carnivores reprend toutes les méthodes des carnivores. Les carnivores sont des animaux qui mangent de la 
    viande et qui peuvent attaquer d'autres animaux. Les carnivores sont des sortes d'animaux, ce sont donc des formes de 
    vies et donc des items.

    Classe mère : Animal
    Classes filles : Tyrannosaure, Velociraptor
    """
    def __init__(self, line, column):
        """
        Les Carnivores ont les instances de la classe Animal.

        Entrées : instances de la classe Animal, la ligne et la colonne du carnivore
        Sorties : /
        """
        Animal.__init__(self, line, column)
        self.attack_damage = 1


    def attack(self):
        """
        Cette fonctio permet aux carnivores d'attaques d'autres animaux dans le but de se nourir de leur viande quand ils
        sont morts. Les carnivores ne peuvent attaquer que si les autres animaux sont dans leur zone de contact. Ils 
        n'attaquent pas des animaux de leur propre espèce.

        Entrées : instances de la classe Carnivore
        Sorties : /
        """
        board = world.get_board()
        vision = Zone(board, self.line, self.column)
        contact_zone = vision.contact_zone()
        my_carnivore = board[self.line][self.column]
        cases = []
        if type(my_carnivore) != type(Meat):          
            for case in contact_zone:
                item = board[case[0]][case[1]]
                if isinstance(item, Animal) and not isinstance(item, type(my_carnivore)):
                    cases += [case]       
            if cases !=[]:
                case = random.choice(cases)
                proie = board[case[0]][case[1]]
                proie.health -= self.attack_damage     
                print("le carnivore",my_carnivore ,"à la case", self.line, self.column, "attaque l'animal",proie, "à la case", case[0],case[1])
                print("la proie",proie,"perd", self.attack_damage, "points de vie, elle n'a plus que", proie.health,"points de vie")
                self.already_played = "YES"


        
    def feed(self):
        """
        Cette fonction s'occupe de l'alimentation des carnivores : ils mangent de la viande dans leur zone de contact.

        Entrées : instances de la classe Carnivore
        Sorties : /
        """
        board = world.get_board()
        vision = Zone(board, self.line, self.column)
        contact_zone = vision.contact_zone()
        my_carnivore = board[self.line][self.column]
        cases = []
        for case in contact_zone:
            item = board[case[0]][case[1]]
            if isinstance(item, Meat) and item.waitaround=="YES":
                cases += [case]
        if cases !=[]:
            case = random.choice(cases)
            world.remove_item(case[0],case[1])
            self.energy += 10
            print("le carnivore", my_carnivore,"a la case", self.line, self.column ,"a mangé la viande a la case", case[0],case[1])
            self.already_played = "YES"



    def move(self):
        """
        Cette fonction s'occupe de faire bouger les animaux sur le plateau.
        Les animaux vont se déplacer de manière intelligente : 
            Les carnivores vont se rapprocher de la viande et des autres animaux pour les attaquer ou d'un carnivore de son espèce
            du sexe opposé pour se reproduire, si ils ne voient ni viandes ni animaux dans leurs champ de vision, ils se déplacent aléatoirement.
        Les animaux se déplacent dans leurs zone de déplacement.

        Entrées : instances de la classe Carnivore
        Sorties : /
        """
        if self.already_played == "NO":
            board = world.get_board()
            zone = Zone(board, self.line, self.column)
            vision_zone = zone.vision_en_cercle(self.vision)                # toutes les cases que les animaux peuvent voir
            move_zone = zone.move_zone()                    # toutes les cases dans lesquelles les animaux peuvent se déplacer
            my_animal = board[self.line][self.column]
            cases_with_meat = []
            cases_with_proie = []
            cases_reproduction = []

            for case in vision_zone:
                item = board[case[0]][case[1]]
                if isinstance(item, Meat):
                    cases_with_meat += [case]
                elif isinstance(item, Animal) and type(item) != type(my_animal):
                    cases_with_proie += [case]
                elif type(item) == type(my_animal):
                    if item.genre != self.genre:
                        cases_reproduction += [case]

            
            optimal_cases = []
            if cases_with_meat != []:               # par ordre de priorité on cherche d'abord les cases avec de la viande
                for case in cases_with_meat:
                    optimal_cases += [case]
                raison = "dans le but de manger de la viande à la case"
            elif cases_reproduction != []:          # puis les cases pour se reproduire
                for case in cases_reproduction:
                    optimal_cases += [case]
                raison = "dans le but de se reproduire avec l'animal à la case"
            elif cases_with_proie != []:            # puis les cases pour attaquer
                for case in cases_with_proie:
                    optimal_cases += [case]
                raison = "dans le but de chasser l'animal à la case"
            
            distance_entre_les_cases = []
            if optimal_cases != []:
                case_to_go = random.choice(optimal_cases)       # la case vers laquelle le carnivore se dirige
                line_case_to_go = case_to_go[0]
                column_case_to_go = case_to_go[1]
                cases_can_move = []
                for case in move_zone:
                    item = board[case[0]][case[1]]
                    if type(item) == type("--"):
                        cases_can_move += [case]

                if cases_can_move != []:
                    for case in cases_can_move:
                        line_case = case[0]
                        column_case = case[1]
                        eloignement = (abs(line_case_to_go -line_case)) + abs(column_case_to_go - column_case)
                        distance_entre_les_cases += [eloignement]
                    
                    case_chosen = cases_can_move[distance_entre_les_cases.index(min(distance_entre_les_cases))]     # la case choisie est celle qui se dirige vers la case que le carnivore vise
                    world.move_item(my_animal, self.line, self.column, case_chosen[0], case_chosen[1])
                    print("le carnivore", my_animal, "à la case", self.line, self.column, "se déplace à la case",case_chosen[0], case_chosen[1], raison, case_to_go[0], case_to_go[1])
                    self.line = case_chosen[0]         
                    self.column = case_chosen[1]
                    self.already_played = "YES"

        # Si l'animal ne sait pas ou aller il bouge aléatoirement
        if self.already_played == "NO":
            cases_can_move = []
            for case in move_zone:
                item = board[case[0]][case[1]]
                if type(item) == type("--"):
                    cases_can_move += [case]
            if cases_can_move != []:
                case_chosen = random.choice(cases_can_move)
                world.move_item(my_animal, self.line, self.column, case_chosen[0], case_chosen[1])
                print("le carnivore", my_animal, "à la case", self.line, self.column, "se déplace à la case",case_chosen[0], case_chosen[1], "mais est un peu perdu car il ne voit rien d'intéressant dans son champ de vision")
                self.line = case_chosen[0]         
                self.column = case_chosen[1]
                self.already_played = "YES"










class Herbivore(Animal):
    """
    La classe Herbivore reprend toutes les méthodes des herbivores. Les herbivores sont des animaux, ce sont des 
    formes de vies et donc des items

    Classe mère : Animal
    Classes filles : Brachiosaure, Stegosaure
    """
    def __init__(self, line, column):
        """
        Les Herbivores ont les instances de la classe Animal.

        Entrées : instances de la classe Animal, la ligne et la colonne de l'herbivore
        Sorties : /
        """
        Animal.__init__(self, line, column)



    def feed(self):
        """
        Cette fonction s'occupe de l'alimentation des herbivores : ils mangent des plantes dans leur zone de contact.

        Entrées : instances de la classe Herbivore
        Sorties : /
        """
        board = world.get_board()
        zone = Zone(board, self.line, self.column)
        contact_zone = zone.contact_zone()
        cases_with_plants = []
        for case in contact_zone:
            if isinstance(board[case[0]][case[1]], Plant):
                if board[case[0]][case[1]].waitaround=="YES":           # attend un tour pour ne pas manger les plantes qui viennent d'être créées
                    cases_with_plants += [case] 
        if cases_with_plants != []:
            case = random.choice(cases_with_plants)
            self.energy += 5
            world.remove_item(case[0],case[1])
            self.already_played = "YES"
            print("l'herbivore a la ligne", self.line, self.column, "a mangé la plante à la case", case)



    def move(self):
        """
        Cette fonction s'occupe de faire bouger les animaux sur les plateaux.
        Les animaux vont se déplacer de manière intelligente : 
            Les herbivores vont se rapprocher des plantes et s'enfuir des carnivores et se rapprocher des herbivores avec qui ils
            peuvent se reproduire. Si ils ne voient aucun des 3 dans leur zone de vision ils se déplaceront aléatoirement.

        Entrées : instances de la classe Herbivore
        Sorties : /
        """
        if self.already_played == "NO":
            board = world.get_board()
            zone = Zone(board, self.line, self.column)
            vision_zone = zone.vision_en_cercle(self.vision)    # toutes les cases que les animaux peuvent voir
            move_zone = zone.move_zone()                        # toutes les cases dans lesquelles les animaux peuvent se déplacer
            my_animal = board[self.line][self.column]
            cases_with_plants = []
            cases_with_carnivore = []
            cases_reproduction = []

            for case in vision_zone:
                item = board[case[0]][case[1]]
                if isinstance(item, Plant):
                    cases_with_plants += [case]
                elif isinstance(item, Carnivore):
                    cases_with_carnivore += [case]
                elif type(item) == type(my_animal):
                    if item.genre != self.genre:
                        cases_reproduction += [case]

            optimal_cases = []
            worst_cases = []
            if cases_with_plants != []:
                for case in cases_with_plants:
                    optimal_cases += [case]
            if cases_with_carnivore != []:
                for case in cases_with_carnivore:
                    worst_cases += [case]
            
            if optimal_cases != []:
                distance_entre_les_cases = []
                for case in optimal_cases:
                    line_case_to_go = case[0]
                    column_case_to_go = case[1]
                    eloignement = (abs(line_case_to_go -self.line)) + abs(column_case_to_go - self.column)
                    distance_entre_les_cases += [eloignement]
                case_chosen_to_eat = optimal_cases[distance_entre_les_cases.index(min(distance_entre_les_cases))]
                distance_case_to_eat = min(distance_entre_les_cases)
                
            if worst_cases != []:
                distance_entre_les_cases = []
                for case in worst_cases:
                    line_case_to_go = case[0]
                    column_case_to_go = case[1]
                    eloignement = (abs(line_case_to_go -self.line)) + abs(column_case_to_go - self.column)
                    distance_entre_les_cases += [eloignement]
                case_chosen_to_fear = worst_cases[distance_entre_les_cases.index(min(distance_entre_les_cases))]
                distance_case_to_fear= min(distance_entre_les_cases)



            # si il y a un autre animal pour se reproduire dans le champ de vision
            if cases_reproduction != []:
                case_chosen = random.choice(cases_reproduction)
                world.move_item(my_animal, self.line, self.column, case_chosen[0], case_chosen[1])
                print("l'herbivore", my_animal, "à la case", self.line, self.column, "se déplace à la case",case_chosen[0], case_chosen[1], "dans le but de se reproduire avec l'animal à la case", case_chosen[0], case_chosen[1])
                self.line = case_chosen[0]         
                self.column = case_chosen[1]
                self.already_played = "YES"


            # manger
            elif worst_cases != [] and optimal_cases != []:
                if distance_case_to_eat < distance_case_to_fear:        # si une plante est plus proche que le predateur le plus proche alors on prend le temps d'aller vers la plante
                    case_to_go = case_chosen_to_eat
                    distance_entre_les_cases = []
                    line_case_to_go = case_to_go[0]
                    column_case_to_go = case_to_go[1]
                    cases_can_move = []
                    for case in move_zone:
                        item = board[case[0]][case[1]]
                        if type(item) == type("--"):
                            cases_can_move += [case]

                    if cases_can_move != []:
                        for case in cases_can_move:
                            line_case = case[0]
                            column_case = case[1]
                            eloignement = (abs(line_case_to_go -line_case)) + abs(column_case_to_go - column_case)
                            distance_entre_les_cases += [eloignement]
                        
                        case_chosen = cases_can_move[distance_entre_les_cases.index(min(distance_entre_les_cases))]     # la case choisie est celle qui se dirige vers la case que le carnivore vise
                        world.move_item(my_animal, self.line, self.column, case_chosen[0], case_chosen[1])
                        print("l'herbivore", my_animal, "à la case", self.line, self.column, "se déplace à la case",case_chosen[0], case_chosen[1], "dans le but de manger la plante à la case", case_to_go[0], case_to_go[1])
                        self.line = case_chosen[0]         
                        self.column = case_chosen[1]
                        self.already_played = "YES"

                # fuir
                else:
                    case_to_go = case_chosen_to_fear
                    distance_entre_les_cases = []
                    line_case_to_go = case_to_go[0]
                    column_case_to_go = case_to_go[1]
                    cases_can_move = []
                    for case in move_zone:
                        item = board[case[0]][case[1]]
                        if type(item) == type("--"):
                            cases_can_move += [case]

                    if cases_can_move != []:
                        for case in cases_can_move:
                            line_case = case[0]
                            column_case = case[1]
                            eloignement = (abs(line_case_to_go -line_case)) + abs(column_case_to_go - column_case)
                            distance_entre_les_cases += [eloignement]
                        
                        case_chosen = cases_can_move[distance_entre_les_cases.index(max(distance_entre_les_cases))]     # la case choisie est celle qui se dirige vers la case que le carnivore vise
                        world.move_item(my_animal, self.line, self.column, case_chosen[0], case_chosen[1])
                        print("l'herbivore", my_animal, "à la case", self.line, self.column, "se déplace à la case",case_chosen[0], case_chosen[1], "dans le but de fuir le carnivore à la case", case_to_go[0], case_to_go[1])
                        self.line = case_chosen[0]         
                        self.column = case_chosen[1]
                        self.already_played = "YES"




        # Si l'animal ne sait pas ou aller il bouge aléatoirement
        if self.already_played == "NO":
            cases_can_move = []
            for case in move_zone:
                item = board[case[0]][case[1]]
                if type(item) == type("--"):
                    cases_can_move += [case]
            if cases_can_move != []:
                case_chosen = random.choice(cases_can_move)
                world.move_item(my_animal, self.line, self.column, case_chosen[0], case_chosen[1])
                print("l'herbivore'", my_animal, "à la case", self.line, self.column, "se déplace à la case",case_chosen[0], case_chosen[1], "mais est un peu perdu car il ne voit rien d'intéressant dans son champ de vision")
                self.line = case_chosen[0]         
                self.column = case_chosen[1]
                self.already_played = "YES"










class Trees(Plant):
    """
    La classe Trees reprend toutes les instances particulières des arbres. Les arbres sont des plantes, donc des
    formes de vies et donc des items.

    Classe mère : Plant
    Classe fille : /
    """
    def __init__(self, line, column):
        """
        Les arbres ont les instances de la classe Plant. Avec quelques particularités pour certaines instances.

        Entrées : instances de la classe Plant, la ligne et la colonne de l'arbre
        Sorties : /
        """
        Plant.__init__(self, line, column)
        self.symbol = "Tr"
        self.health = 10
        self.energy = 20
        self.image = pygame.image.load('assets/tree.png')





class Bush(Plant):   
    """
    La classe Bush reprend toutes les instances particulières des buissons. Les buissons sont des plantes, donc des
    formes de vies et donc des items.

    Classe mère : Plant
    Classe fille : /
    """ 
    def __init__(self, line, column):
        """
        Les buissons ont les instances de la classe Plant. Avec quelques particularités pour certaines instances.

        Entrées : instances de la classe Plant, la ligne et la colonne du buisson.
        Sorties : /
        """
        Plant.__init__(self, line, column)
        self.symbol = "Bu"
        self.health = 10
        self.energy = 15
        self.image = pygame.image.load('assets/bush.png')





class Rose(Plant):
    """
    La classe Rose reprend toutes les instances particulières des roses. Les roses sont des plantes, donc des
    formes de vies et donc des items.

    Classe mère : Plant
    Classe fille : /
    """
    def __init__(self, line, column):
        """
        Les roses ont les instances de la classe Plant. Avec quelques particularités pour certaines instances.

        Entrées : instances de la classe Plant, la ligne et la colonne de la rose.
        Sorties : /
        """
        Plant.__init__(self, line, column)
        self.symbol = "Ro"
        self.health = 20
        self.energy = 5
        self.image = pygame.image.load('assets/rose.png')





class Tyrannosaure(Carnivore):
    """
    La classe Tyrannosaurer reprend toutes les instances particulières des tirannosaures. Les tirannosaures 
    sont des Carnivores, donc des Animaux, donc des formes de vies et donc des items.

    Classe mère : Carnivore
    Classe fille : /
    """
    def __init__(self, line, column):
        """
        Les tyrannosaures ont les instances de la classe Carnivore. Avec quelques particularités pour certaines instances.

        Entrées : instances de la classe Carnivore, la ligne et la colonne du tirannosaure.
        Sorties : /
        """
        Carnivore.__init__(self, line, column)
        self.symbol = "Ty"
        self.health = 20
        self.energy = 20
        self.vision = 5
        self.attack_damage = 4
        self.image = pygame.image.load('assets/tyrannosaure.png')





class Velociraptor(Carnivore):  
    """
    La classe Velociraptor reprend toutes les instances particulières des velociraptors. Les velociraptors
    sont des Carnivores, donc des Animaux, donc des formes de vies et donc des items.

    Classe mère : Carnivore
    Classe fille : /
    """
    def __init__(self, line, column):
        """
        Les velociraptors ont les instances de la classe Carnivore. Avec quelques particularités pour certaines instances.

        Entrées : instances de la classe Carnivore, la ligne et la colonne du velociraptors.
        Sorties : /
        """
        Carnivore.__init__(self, line, column)
        self.symbol = "Ve"
        self.health = 30
        self.energy = 10
        self.attack_damage = 2
        self.image = pygame.image.load('assets/velociraptor.png')
        




class Brachiosaure(Herbivore):
    """
    La classe Brachiosaure reprend toutes les instances particulières des brachiosaures. Les brachiosaures
    sont des Herbivore, donc des Animaux, donc des formes de vies et donc des items.

    Classe mère : Herbivore
    Classe fille : /
    """
    def __init__(self, line, column):
        """
        Les brachiosaures ont les instances de la classe Herbivore. Avec quelques particularités pour certaines instances.

        Entrées : instances de la classe Herbivore, la ligne et la colonne du brachiosaure.
        Sorties : /
        """
        Herbivore.__init__(self, line, column)
        self.symbol = "Br"
        self.health = 50
        self.energy = 20
        self.image = pygame.image.load('assets/brachiosaure.png')





class Stegosaure(Herbivore):
    """
    La classe Stegosaure reprend toutes les instances particulières des stegosaures. Les stegosaures
    sont des Herbivore, donc des Animaux, donc des formes de vies et donc des items.

    Classe mère : Herbivore
    Classe fille : /
    """
    def __init__(self, line, column):
        """
        Les stegosaures ont les instances de la classe Herbivore. Avec quelques particularités pour certaines instances.

        Entrées : instances de la classe Herbivore, la ligne et la colonne du stegosaures.
        Sorties : /
        """
        Herbivore.__init__(self, line, column)
        self.symbol = "St"
        self.health = 30                             
        self.energy = 30
        self.vision = 5
        self.image = pygame.image.load('assets/stegosaure.png')











class Zone:
    """
    La classe Zone reprend toutes les méthodes des zones.

    Classe mère : /
    Classe fille : /
    """
    def __init__(self, board, line, column):
        """
        Les zones ont les instances suivantes : le plateau de jeu, la ligne et la colonne de l'item dont on parle.

        Entrées : instances de la classe Zone, le plateau de jeu, la ligne et la colonne de l'item dont on parle.
        Sorties : /
        """
        self.board = board
        self.line = line
        self.column = column


    def vision_en_cercle(self, rayon):
        """
        Cette fonction s'occupe de créer une zone de vision circulaire autour d'une case.
        Elle renvoie toutes les cases qui sont dans la zone de vision.

        Cette fonction retourne la zone de vision dans laquelle un animal peut voir:
            La zone de vision est la zone dans laquelle un animal peut voir (des proies, de la nourriture, des prédateurs).
        
        mais aussi la zone de racine :
            Pour les plantes, la zone de racines est la zone dans laquelle elle peut consommer les déchets organiques.
            Cette fonction renvoie la zone de racines des plantes.

        et aussi la zone de semis : 
            Pour les plantes, la zone de semis est la zone dans laquelle de nouvelles plantes peuvent apparaître autour d'une plante existante.
            Cette fonction renvoie la zone de semis des plantes.

        Entrée : instances de la classe Zone et le rayon de la zone que l'on veut
        Sortie : liste des cases qui appartiennent à la zone de vision.
        """
        i = 1
        list_line = [self.line]
        list_column = [self.column]
        cases = []
        while i <= rayon:
            list_line += [i + self.line]
            list_line += [-i + self.line]
            i+=1
        j = 1
        while j <= rayon:
            list_column += [j +self.column]
            list_column += [-j + self.column]
            j+=1

        for x in list_line:
            for y in list_column:
                case = [x,y]
                if math.sqrt((x-self.line)**2 +(y-self.column)**2) <= rayon:
                    if x in range(len(self.board)) and y in range(len(self.board[0])):
                        cases+=[case]
        cases.remove([self.line, self.column])
        return cases



    def contact_zone(self):
        """
        La zone de contact est la zone dans laquelle on considère que le contact est possible. 
        Un prédateur peut attaquer une proie. Un herbivore peut manger une plante. Un mâle et une femelle peuvent se reproduire...
        Cette fonction renvoie la zone de contact.
        Cette fonction est séparée de la fonction vision en cercle pour ne pas pouvoir choisir la zone de contact : la zone de contact 
        est toujours les cases autour de l'item.

        Entrées : instances de la classe Zone.
        Sorties : une liste des cases ou l'animal peut entrer en contacte (matrice).
        """
        l = self.line
        c = self.column
        list_cases = []
        porte = 1                                   # contact j'usqu'a 1 cases autour
        for i in range(l-porte,l+porte+1):
            for j in range(c-porte,c+porte+1):
                list_cases += [[i,j]]
        contact_zone = []

        for case in list_cases:
            if case[0] in range(len(self.board)) and case[1] in range(len(self.board[0])):
                contact_zone += [case]
        return contact_zone



    def move_zone(self):
        """
        Cette fonction renvoie une zone dans laquel les animaux peuvent bouger.
        Cette zone est 1 case autour, attention de pas augmenter la zone car les fontions move des animaux n'ont pas
        été conçues pour une zone plus grande.

        Entrée : instances de la classe Zone.
        Sorties : une liste des cases ou l'annimal peut se déplacer (matrice).
        """
        l = self.line
        c = self.column
        list_cases = []
        porte = 1                                       # peut se déplacer 1 case autour
        for i in range(l-porte,l+porte+1):
            for j in range(c-porte,c+porte+1):
                list_cases += [[i,j]]
        move_zone = []

        for case in list_cases:
            if case[0] in range(len(self.board)) and case[1] in range(len(self.board[0])):
                move_zone += [case]
        return move_zone

# CODE PRINCIPAL

print("Bienvenue")
world = World()
pygame.init()
pygame.display.set_caption("Jurrasic World")
screen = pygame.display.set_mode((800, 800))
background = pygame.image.load('assets/background.jpg')
screen.blit(background,(0, 0))
pygame.display.flip()
time.sleep(2)
running = True
nb=1
i=1
while running:

    print("tour numéro {}".format(i))
    screen.blit(background,(0, 0))
    world.round()
    for line in world.board:
            for item in line:
                if isinstance(item, Item) :
                    symbol = pygame.transform.scale(item.image, (80, 80))
                    screen.blit(symbol,(80*item.column, 80*item.line))

    pygame.display.flip()
    time.sleep(1)           #### détermine le temps d'un round (retirer la ligne pour une partie rapide)
    i+=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")