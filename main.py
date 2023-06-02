"""
Modèle de départ pour la programmation Arcade.
Il suffit de modifier les méthodes nécessaires à votre jeu.
"""

#Importation des modules
import random

import arcade

import game_state
#import arcade.gui


#Importation de attack_animation.py et game_state.py
from attack_animation import AttackType, AttackAnimation
from game_state import GameState

#Définir les Constantes
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45  # The default line height for text.

#Définir les classes
class MyGame(arcade.Window):
   """
   La classe principale de l'application

   NOTE: Vous pouvez effacer les méthodes que vous n'avez pas besoin.
   Si vous en avez besoin, remplacer le mot clé "pass" par votre propre code.
   """
#Définir les paramètres des images
   PLAYER_IMAGE_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
   PLAYER_IMAGE_Y = SCREEN_HEIGHT / 2.5
   COMPUTER_IMAGE_X = (SCREEN_WIDTH / 2) * 1.5
   COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 2.5
   ATTACK_FRAME_WIDTH = 154 / 2
   ATTACK_FRAME_HEIGHT = 154 / 2

   def __init__(self, width, height, title):
       super().__init__(width, height, title)
#Définir la couleur de l'arrière-plan
       arcade.set_background_color(arcade.color.BLACK_OLIVE)
#Définir les variables
       self.player = None
       self.computer = None
       self.players = None
       self.rock = None
       self.paper = None
       self.scissors = None
       self.player_score = 0
       self.computer_score = 0
       self.player_attack_type = {}
       self.computer_attack_type = None
       self.player_attack_chosen = False
       self.player_won_round = None
       self.draw_round = None
       self.game_state = game_state.GameState.NOT_STARTED
       self.attack_list = arcade.SpriteList()
       self.affichage_text = None

   def setup(self):
       """
       Configurer les variables de votre jeu ici. Il faut appeler la méthode une nouvelle
       fois si vous recommencer une nouvelle partie.
       """
       # C'est ici que vous allez créer vos listes de sprites et vos sprites.
       # Prenez note que vous devriez attribuer une valeur à tous les attributs créés dans __init__

       # Créer les sprites pour le joueur et l'ordinateur
       self.player = arcade.Sprite("assets/faceBeard.png", 0.5)
       self.player.center_x = self.PLAYER_IMAGE_X
       self.player.center_y = self.PLAYER_IMAGE_Y
       self.computer = arcade.Sprite("assets/compy.png", 2.5)
       self.computer.center_x = self.COMPUTER_IMAGE_X
       self.computer.center_y = self.COMPUTER_IMAGE_Y
       self.players = arcade.SpriteList()
       self.players.append(self.player)
       self.players.append(self.computer)

       # Créer les dictionnaires pour les attaques
       self.player_attack_type = {AttackType.ROCK: self.rock, AttackType.PAPER: self.paper, AttackType.SCISSORS: self.scissors}
       self.computer_attack_type = random.randint(1, 3)

       # Créer les variables pour les scores
       self.player_score = 0
       self.computer_score = 0
       self.affichage_text = True

       # Créer les variables pour les états de jeu
       self.player_attack_chosen = False
       self.player_won_round = None
       self.draw_round = False
       self.game_state = game_state.GameState.NOT_STARTED

       # Créer les sprites pour les attaques
       self.rock = arcade.Sprite("assets/srock.png", 0.5)
       self.rock_attack = arcade.Sprite("assets/srock-attack.png", 0.5)
       self.paper = arcade.Sprite("assets/spaper.png", 0.5)
       self.paper_attack = arcade.Sprite("assets/spaper-attack.png", 0.5)
       self.scissors = arcade.Sprite("assets/scissors.png", 0.5)
       self.scissors_attack = arcade.Sprite("assets/scissors-close.png", 0.5)

#Valider la victoire
   def validate_victory(self):
       """
       Utilisé pour déterminer qui obtient la victoire (ou s'il y a égalité)
       Rappel: après avoir validé la victoire, il faut changer l'état de jeu
       """
       #Si le joueur gagne
       if self.player_score == 3:
           self.game_state = game_state.GameState.PLAYER_WON

       #Si l'ordinateur gagne
       elif self.computer_score == 3:
           self.game_state = game_state.GameState.COMPUTER_WON

#Dessiner les attaques du joueur
   def draw_possible_attack(self):
       #Dessiner les rectangles contenants les attaques
       arcade.draw_rectangle_outline(100, 100, 75, 75, arcade.color.RED, 4)
       arcade.draw_rectangle_outline(250, 100, 75, 75, arcade.color.RED, 4)
       arcade.draw_rectangle_outline(400, 100, 75, 75, arcade.color.RED, 4)
       #Dessiner les attaques
       if self.player_attack_chosen == False and self.game_state == game_state.GameState.ROUND_ACTIVE:
           #Dessiner la roche
           self.rock.center_x = 100
           self.rock.center_y = 100
           self.rock.draw()
           #Dessiner le papier
           self.paper.center_x = 250
           self.paper.center_y = 100
           self.paper.draw()
           #Dessiner les ciseaux
           self.scissors.center_x = 400
           self.scissors.center_y = 100
           self.scissors.draw()
       #Afficher uniquement l'attaque choisie
       if self.player_attack_chosen == True and self.game_state == game_state.GameState.ROUND_ACTIVE:
           #Si la roche est choisie
           if self.player_attack_type == AttackType.ROCK:
               self.rock_attack.center_x = 100
               self.rock_attack.center_y = 100
               self.rock_attack.draw()
           #Si le papier est choisi
           if self.player_attack_type == AttackType.PAPER and self.player_attack_chosen == True and self.game_state == game_state.GameState.ROUND_ACTIVE:
               self.paper_attack.center_x = 250
               self.paper_attack.center_y = 100
               self.paper_attack.draw()
           #Si les ciseaux sont choisis
           if self.player_attack_type == AttackType.SCISSORS and self.player_attack_chosen == True and self.game_state == game_state.GameState.ROUND_ACTIVE:
                self.scissors_attack.center_x = 400
                self.scissors_attack.center_y = 100
                self.scissors_attack.draw()

#Dessiner les attaques de l'ordinateur
   def draw_computer_attack(self):
       """
       Méthode utilisée pour dessiner les possibilités d'attaque de l'ordinateur
       """

       #Dessiner le rectangle contenant l'attaque
       arcade.draw_rectangle_outline(770, 100, 75, 75, arcade.color.RED, 4)
       #Pour la roche
       if self.computer_attack_type == 1 and self.player_attack_chosen == True:
           self.rock.center_x = 770
           self.rock.center_y = 100
           self.rock.draw()
       #Pour le papier
       if self.computer_attack_type == 2 and self.player_attack_chosen == True:
           self.paper.center_x = 770
           self.paper.center_y = 100
           self.paper.draw()
       #Pour les ciseaux
       if self.computer_attack_type == 3 and self.player_attack_chosen == True:
           self.scissors.center_x = 770
           self.scissors.center_y = 100
           self.scissors.draw()

#Dessiner les scores du joueur et de l'ordinateur
   def draw_scores(self):
       """
       Montrer les scores du joueur et de l'ordinateur
       """
       if self.game_state == game_state.GameState.ROUND_ACTIVE:
            arcade.draw_text("Player: " + str(self.player_score), 220, 350, arcade.color.WHITE, 14)
            arcade.draw_text("Computer: " + str(self.computer_score), 720, 350, arcade.color.WHITE, 14)
       pass

#Dessiner les instructions
   def draw_instructions(self):
       """
       Dépendemment de l'état de jeu, afficher les instructions d'utilisation au joueur (appuyer sur espace, ou sur une image)
       """
       #Si le jeu n'est pas commencé
       if self.game_state == game_state.GameState.NOT_STARTED:
           arcade.draw_text("Appuyer sur espace pour commencer", 430, 300, arcade.color.WHITE, 14)
       #Si le jeu est commencé et que le joueur a gagné la manche
       if self.game_state == game_state.GameState.PLAYER_WON:
           arcade.draw_text("You won! Press space to restart", 10, 50, arcade.color.WHITE, 14)
       #Si le jeur est commencé et que l'ordinateur a gagné la manche
       if self.game_state == game_state.GameState.COMPUTER_WON:
              arcade.draw_text("You lost! Press space to restart", 10, 50, arcade.color.WHITE, 14)
       #Si le jeu est commencé et que le joueur n'a pas choisi son attaque
       if self.game_state == game_state.GameState.ROUND_ACTIVE:
           arcade.draw_text("Choisisez votre attack en cliquant dessus", 380, 250, arcade.color.WHITE, 10)
       arcade.draw_text("", 10, 70, arcade.color.WHITE, 14)
       pass

       #Instruction et reset de manche pour chaque possibilité d'attaque

       #Si le joueur choisit la roche et que l'ordinateur choisit la roche
       if self.player_attack_chosen == True and self.player_attack_type == AttackType.ROCK and self.computer_attack_type == 1:
           self.reset_round()
           while self.affichage_text == True:
               arcade.draw_text("Égalité! Appuyer sur espace pour continuer", 350, 400, arcade.color.WHITE, 14)
       #Si le joueur choisit la roche et que l'ordinateur choisit le papier
       if self.player_attack_chosen == True and self.player_attack_type == AttackType.ROCK and self.computer_attack_type == 2:
           self.computer_score = self.computer_score + 1
           self.reset_round()
           while self.affichage_text == True:
               arcade.draw_text("Vous avez perdu! Appuyer sur espace pour continuer", 350, 400, arcade.color.WHITE, 14)
       #Si le joueur choisit la roche et que l'ordinateur choisit les ciseaux
       if self.player_attack_chosen == True and self.player_attack_type == AttackType.ROCK and self.computer_attack_type == 3:
           self.player_score = self.player_score + 1
           self.reset_round()
           while self.affichage_text == True:
               arcade.draw_text("Vous avez gagné! Appuyer sur espace pour continuer", 350, 400, arcade.color.WHITE, 14)
       #Si le joueur choisit le papier et que l'ordinateur choisit la roche
       if self.player_attack_chosen == True and self.player_attack_type == AttackType.PAPER and self.computer_attack_type == 1:
           self.player_score = self.player_score + 1
           self.reset_round()
           while self.affichage_text == True:
               arcade.draw_text("Vous avez gagné! Appuyer sur espace pour continuer", 350, 400, arcade.color.WHITE, 14)
       #Si le joueur choisit le papier et que l'ordinateur choisit le papier
       if self.player_attack_chosen == True and self.player_attack_type == AttackType.PAPER and self.computer_attack_type == 2:
           self.reset_round()
           while self.affichage_text == True:
               arcade.draw_text("Égalité! Appuyer sur espace pour continuer", 350, 400, arcade.color.WHITE, 14)
       #Si le joueur choisit le papier et que l'ordinateur choisit les ciseaux
       if self.player_attack_chosen == True and self.player_attack_type == AttackType.PAPER and self.computer_attack_type == 3:
           self.computer_score = self.computer_score + 1
           self.reset_round()
           while self.affichage_text == True:
               arcade.draw_text("Vous avez perdu! Appuyer sur espace pour continuer", 350, 400, arcade.color.WHITE, 14)
       #Si le joueur choisit les ciseaux et que l'ordinateur choisit la roche
       if self.player_attack_chosen == True and self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == 1:
           self.computer_score = self.computer_score + 1
           self.reset_round()
           while self.affichage_text == True:
               arcade.draw_text("Vous avez perdu! Appuyer sur espace pour continuer", 350, 400, arcade.color.WHITE, 14)
       #Si le joueur choisit les ciseaux et que l'ordinateur choisit le papier
       if self.player_attack_chosen == True and self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == 2:
           self.player_score = self.player_score + 1
           self.reset_round()
           while self.affichage_text == True:
               arcade.draw_text("Vous avez gagné! Appuyer sur espace pour continuer", 350, 400, arcade.color.WHITE, 14)
       #Si le joueur choisit les ciseaux et que l'ordinateur choisit les ciseaux
       if self.player_attack_chosen == True and self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == 3:
           self.reset_round()
           while self.affichage_text == True:
               arcade.draw_text("Égalité! Appuyer sur espace pour continuer", 350, 400, arcade.color.WHITE, 14)


#Affichage du jeu
   def on_draw(self):
       """
       C'est la méthode que Arcade invoque à chaque "frame" pour afficher les éléments
       de votre jeu à l'écran.
       """

       # Cette commande permet d'effacer l'écran avant de dessiner. Elle va dessiner l'arrière
       # plan selon la couleur spécifié avec la méthode "set_background_color".
       arcade.start_render()

       # Display title
       arcade.draw_text(SCREEN_TITLE,
                        0,
                        SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
                        arcade.color.BLACK_BEAN,
                        60,
                        width=SCREEN_WIDTH,
                        align="center")
#Appeler les méthodes pour afficher les éléments du jeu
       self.draw_instructions()
       self.players.draw()
       self.draw_possible_attack()
       self.draw_scores()
       self.draw_computer_attack()

       #afficher l'attaque de l'ordinateur selon l'état de jeu
       #afficher le résultat de la partie si l'ordinateur a joué (ROUND_DONE)
       pass

#Mettre à jour le jeu
   def on_update(self, delta_time):
       """
       Toute la logique pour déplacer les objets de votre jeu et de
       simuler sa logique vont ici. Normalement, c'est ici que
       vous allez invoquer la méthode "update()" sur vos listes de sprites.
       Paramètre:
           - delta_time : le nombre de milliseconde depuis le dernier update.
       """
       #vérifier si le jeu est actif (ROUND_ACTIVE) et continuer l'animation des attaques
       if self.game_state == game_state.GameState.ROUND_ACTIVE:
           if self.player_attack_chosen == True:
               pass

       #si le joueur a choisi une attaque, générer une attaque de l'ordinateur et valider la victoire
       #changer l'état de jeu si nécessaire (GAME_OVER)
       pass

#Si espace est pessé
   def on_key_press(self, key, key_modifiers):
       """
       Cette méthode est invoquée à chaque fois que l'usager tape une touche
       sur le clavier.
       Paramètres:
           - key: la touche enfoncée
           - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?

       Pour connaître la liste des touches possibles:
       http://arcade.academy/arcade.key.html
       """
#Commencer le jeu si espace est pressé
       if (self.game_state == game_state.GameState.NOT_STARTED and key == arcade.key.SPACE):
           self.game_state = game_state.GameState.ROUND_ACTIVE
#Enlever le texte énonçant le gagnant de la manche si espace est pressé
       if self.game_state == game_state.GameState.ROUND_DONE and key == arcade.key.SPACE:
           self.affichage_text = False

       pass
#Reset la manche
   def reset_round(self):
       """
       Réinitialiser les variables qui ont été modifiées
       """
       #Reset les paramètres de la manche
       self.computer_attack_type = random.randint(1, 3)
       self.player_attack_chosen = False
       self.player_attack_type = {AttackType.ROCK: False, AttackType.PAPER: False, AttackType.SCISSORS: False}
       self.player_won_round = False
       self.draw_round = False
       self.game_state = game_state.GameState.ROUND_DONE

       #Si le joueur a gagné la partie, afficher le texte approprié
       if self.game_state == game_state.GameState.PLAYER_WON:
           self.game_state = game_state.GameState.GAME_OVER
           self.player_score = 0
           self.computer_score = 0
           arcade.draw_text("Vous avez gagné la parti! Appuyer sur espace pour rejouer", 350, 400, arcade.color.WHITE, 14)
       #Si le joueur a perdu la partie, afficher le texte approprié
       if self.game_state == game_state.GameState.COMPUTER_WON:
           self.game_state = game_state.GameState.GAME_OVER
           self.player_score = 0
           self.computer_score = 0
           arcade.draw_text("Vous avez perdu la parti! Appuyer sur espace pour rejouer", 350, 400, arcade.color.WHITE, 14)


       pass

#Si la souris est cliquée
   def on_mouse_press(self, x, y, button, key_modifiers):
       """
       Méthode invoquée lorsque l'usager clique un bouton de la souris.
       Paramètres:
           - x, y: coordonnées où le bouton a été cliqué
           - button: le bouton de la souris appuyé
           - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
       """
       #Si le jeu est actif, vérifier si le joueur a cliqué sur une des attaques
       if self.game_state == game_state.GameState.ROUND_ACTIVE:
           if self.rock.collides_with_point((x, y)):
               self.player_attack_type = AttackType.ROCK
               self.player_attack_chosen = True
           elif self.paper.collides_with_point((x, y)):
               self.player_attack_type = AttackType.PAPER
               self.player_attack_chosen = True
           elif self.scissors.collides_with_point((x, y)):
               self.player_attack_type = AttackType.SCISSORS
               self.player_attack_chosen = True

       # Test de collision pour le type d'attaque (self.player_attack_type).
       # Rappel que si le joueur choisi une attaque, self.player_attack_chosen = True




#Méthode principale
def main():
   """ Main method """
   game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
   game.setup()
   arcade.run()

#Commencer le jeu
if __name__ == "__main__":
   main()
