import pygame
import math
from boardGame import BoardGame
from player import Player

pygame.init()

class Game:
    def __init__(self):
        self.board = BoardGame()
        self.player1 = Player("Player 1", "red")
        self.player2 = Player("Player 2", "black")
        self.turn = self.player1
        self.gameover = False
        self.selected_piece = None

    def switch_turn(self):
        self.turn = self.player1 if self.turn == self.player2 else self.player2