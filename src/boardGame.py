import pygame
import math
pygame.init()

class BoardGame:
    def __init__(self, width=700, height=700):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Cờ Tướng")
        
        #màu
        self.BG_COLOR = (244, 164, 96)
        self.LINE_COLOR = (0, 0, 0)
        self.BLACK_PIECE = (0, 0, 0)
        self.RED_PIECE = (255, 0, 0)
        
        #size
        self.cell_size = 60
        self.board_width = 8 * self.cell_size
        self.board_height = 9 * self.cell_size
        self.offset_x = (self.width - self.board_width) // 2
        self.offset_y = (self.height - self.board_height) // 2
        
        # Font chữ Hán
        self.font = pygame.font.SysFont("SimSun", 40)
        
        self.piece_symbols = {
            "K_b": "將", "K_r": "帥",  # Tướng
            "A_b": "士", "A_r": "仕",  # Sĩ
            "E_b": "象", "E_r": "相",  # Tượng
            "R_b": "車", "R_r": "俥",  # Xe
            "N_b": "馬", "N_r": "傌",  # Mã
            "C_b": "砲", "C_r": "炮",  # Pháo
            "P_b": "卒", "P_r": "兵"   # Tốt
        }
        
        
        self.pieces = [
            ("K_b", (0, 4)), ("A_b", (0, 3)), ("A_b", (0, 5)), ("E_b", (0, 2)), ("E_b", (0, 6)),
            ("R_b", (0, 0)), ("R_b", (0, 8)), ("N_b", (0, 1)), ("N_b", (0, 7)),
            ("C_b", (2, 1)), ("C_b", (2, 7)), ("P_b", (3, 0)), ("P_b", (3, 2)),
            ("P_b", (3, 4)), ("P_b", (3, 6)), ("P_b", (3, 8)),
            
            ("K_r", (9, 4)), ("A_r", (9, 3)), ("A_r", (9, 5)), ("E_r", (9, 2)), ("E_r", (9, 6)),
            ("R_r", (9, 0)), ("R_r", (9, 8)), ("N_r", (9, 1)), ("N_r", (9, 7)),
            ("C_r", (7, 1)), ("C_r", (7, 7)), ("P_r", (6, 0)), ("P_r", (6, 2)),
            ("P_r", (6, 4)), ("P_r", (6, 6)), ("P_r", (6, 8))
        ]
        
        # Biến kéo thả
        self.dragging = False
        self.dragged_piece_index = None 
        self.dragged_pos = None         

    def draw_board(self):
        self.screen.fill(self.BG_COLOR)
        for row in range(10):
            y = self.offset_y + row * self.cell_size
            pygame.draw.line(self.screen, self.LINE_COLOR, 
                           (self.offset_x, y), (self.offset_x + self.board_width, y), 2)
        for col in range(9):
            x = self.offset_x + col * self.cell_size
            pygame.draw.line(self.screen, self.LINE_COLOR, 
                           (x, self.offset_y), (x, self.offset_y + self.board_height), 2)
        river_y_top = self.offset_y + 4 * self.cell_size
        pygame.draw.rect(self.screen, (135, 206, 235), 
                        (self.offset_x, river_y_top, self.board_width, self.cell_size))
        for side in [(0, 2), (7, 9)]:
            for col in [3, 5]:
                x1 = self.offset_x + col * self.cell_size
                y1 = self.offset_y + side[0] * self.cell_size
                x2 = self.offset_x + 4 * self.cell_size
                y2 = self.offset_y + side[1] * self.cell_size
                pygame.draw.line(self.screen, self.LINE_COLOR, (x1, y1), (x2, y2), 2)

    def draw_pieces(self):
        piece_radius = self.cell_size // 2 - 5
        
        for i, (piece, (row, col)) in enumerate(self.pieces):
            color = self.BLACK_PIECE if "_b" in piece else self.RED_PIECE
            symbol = self.piece_symbols[piece]
            
            if self.dragging and i == self.dragged_piece_index:
                x, y = self.dragged_pos
            else:
                x = self.offset_x + col * self.cell_size
                y = self.offset_y + row * self.cell_size
            
            pygame.draw.circle(self.screen, color, (x, y), piece_radius)
            pygame.draw.circle(self.screen, self.LINE_COLOR, (x, y), piece_radius, 2)
            text = self.font.render(symbol, True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)

    def get_board_pos(self, mouse_pos):
        x, y = mouse_pos
        col = (x - self.offset_x) // self.cell_size
        row = (y - self.offset_y) // self.cell_size
        if 0 <= col <= 8 and 0 <= row <= 9:
            return (row, col)
        return None

    def find_piece_at_pos(self, mouse_pos):
        mx, my = mouse_pos
        for i, (piece, (row, col)) in enumerate(self.pieces):
            px = self.offset_x + col * self.cell_size
            py = self.offset_y + row * self.cell_size
            distance = math.sqrt((mx - px) ** 2 + (my - py) ** 2)
            if distance < self.cell_size // 2:  # Nếu chuột gần tâm quân cờ
                return i
        return None

    def handle_mouse_down(self, pos):
        piece_index = self.find_piece_at_pos(pos)
        if piece_index is not None:
            self.dragging = True
            self.dragged_piece_index = piece_index
            self.dragged_pos = pos

    def handle_mouse_up(self, pos):
        if not self.dragging or self.dragged_piece_index is None:
            return
        
        new_pos = self.get_board_pos(pos)
        if new_pos:
            row, col = new_pos
            piece_key, _ = self.pieces[self.dragged_piece_index]
            
            # ăn quân
            for i, (other_piece, (r, c)) in enumerate(self.pieces):
                if i != self.dragged_piece_index and (r, c) == (row, col):
                    self.pieces.pop(i)
                    break
            
            # Cập nhật vị trí mới
            self.pieces[self.dragged_piece_index] = (piece_key, (row, col))
        
        self.dragging = False
        self.dragged_piece_index = None
        self.dragged_pos = None

    def handle_mouse_motion(self, pos):
        if self.dragging and self.dragged_piece_index is not None:
            self.dragged_pos = pos

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
            
            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    game = BoardGame()
    game.run()