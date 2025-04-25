import pygame
import math
import gui

from gui import *
from boardGame import BoardGame
from player import Player

pygame.init()

class Game:
    def __init__(self):
        self.cell_size = 60
        self.board_width = self.cell_size * 9 # 540: 9 ô ngang
        self.board_height = self.cell_size * 10 # 600: 10 ô dọc
        self.sidebar_width = 200 # chiều ngang của sidebar 

        self.width = self.board_width + self.sidebar_width
        self.height = self.board_height

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cờ Tướng")

        self.player1 = Player("Player 1", "red")
        self.player2 = Player("Player 2", "black")
        self.board = BoardGame(self)
        self.running = True

        self.turn = self.player1  # Đỏ đi trước
        self.gameover = False

        # các nút bên side bar
        self.buttons = [
            # tạm thời đặt text tiếng anh
            Button(self.board_width + 20, 100, 160, 40, "Reset", self.board.reset_game),
            Button(self.board_width + 20, 160, 160, 40, "Flip Board", self.board.flip_board)
        ]

        # Load ảnh cho sidebar
        self.sidebar_image = pygame.image.load("./assets/images/caytre.jpg")
        # chỉnh lại kích thước cho ảnh
        self.sidebar_image = pygame.transform.scale(self.sidebar_image, 
                                                    (self.sidebar_width, self.height))

    def switch_turn(self):
        self.turn = self.player1 if self.turn == self.player2 else self.player2

        # if self.board.is_in_check(self.turn.color):
        if self.board.is_in_check(self.player1.color):
            if self.board.is_checkmate(self.turn):
                self.gameover = True
                self.board.end_sound.play()
        elif self.board.is_in_check(self.player2.color):
            if self.board.is_checkmate(self.turn):
                self.gameover = True
                self.board.end_sound.play()
                

    def get_opponent(self):
        return self.player1 if self.turn == self.player2 else self.player2

    def handle_events(self):
        for event in pygame.event.get():
            # nếu là nút thoát 
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                # chạy sự kiện nút trong mảng buttons
                for button in self.buttons:
                    if button.handle_event(event):
                        return
                self.board.handle_mouse_event(event)

    

    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))

            self.handle_events()
            self.board.draw()

            if self.gameover:
                gui.show_gameover(self.screen, self.get_opponent().color, self.board.reset_game)

            # Vẽ ảnh lên sidebar
            self.screen.blit(self.sidebar_image, (self.board_width, 0))

            # vẽ nút
            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    # khởi tạo màn hình cho game
    screen = pygame.display.set_mode((740, 600))
    game = Game()
    gui.show_main_menu(screen)
    game.run()
