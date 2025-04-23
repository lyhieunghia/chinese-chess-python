import pygame
import math

import gui
from boardGame import BoardGame
from player import Player

pygame.init()

class Game:
    def __init__(self):

        # Khởi tạo màn hình
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cờ Tướng")
        
        # Khởi tạo các thành phần trò chơi
        self.player1 = Player("Player 1", "red")
        self.player2 = Player("Player 2", "black")
        self.board = BoardGame(self)
        self.running = True
        
        self.turn = self.player1
        self.gameover = False
        

    def switch_turn(self):
        """Chuyển lượt chơi giữa hai người chơi"""
        self.turn = self.player1 if self.turn == self.player2 else self.player2

        if self.board.is_checkmate(self.turn):
            self.gameover = True
    
    def get_opponent(self):
        return self.player1 if self.turn == self.player2 else self.player2

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                self.board.handle_mouse_event(event)

    def run(self):
        """Vòng lặp chính của trò chơi"""
        while self.running:
            self.screen.fill((255, 255, 255))  # Xóa màn hình trước khi vẽ lại
            
            self.handle_events()
            self.board.draw()
            if self.gameover:
                gui.show_gameover(self.screen, self.get_opponent().color)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()