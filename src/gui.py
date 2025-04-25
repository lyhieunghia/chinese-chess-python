import pygame 
import sys


# Lớp nút đơn giản
class Button:
    # x: tọa độ ngang( vị trí )
    # y: tọa độ dọc
    # w: chiều ngang nút
    # h: chiều dọc nút
    # text: chữ hiện trên nút
    # callback: hàm được gọi để xử lý sự kiện
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = (200, 200, 200)
        self.callback = callback
        self.font = pygame.font.SysFont(None, 28)

    def draw(self, surface):
        # Vẽ màu nền của nút, có bo góc 6px
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)

        # Vẽ viền đen xung quanh nút
        pygame.draw.rect(surface, (0, 0, 0), self.rect, width=2, border_radius=6)

        # Vẽ chữ lên nút
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False
    

def show_gameover(screen, winner_color, reset_callback):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    width, height = screen.get_size()

    # Nền mờ đơn giản
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    # Dòng chữ "Đỏ thắng" hoặc "Đen thắng"
    message = f"{'Red' if winner_color == 'red' else 'Black'} win!!!"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))

    # Tạo hai nút
    button_width = 140
    button_height = 50
    spacing = 40

    play_again_rect = pygame.Rect(width // 2 - button_width - spacing // 2, height // 2 + 10, button_width, button_height)
    quit_rect = pygame.Rect(width // 2 + spacing // 2, height // 2 + 10, button_width, button_height)

    play_again_text = small_font.render("Play again", True, (0, 0, 0))
    quit_text = small_font.render("Quit", True, (0, 0, 0))

    play_again_text_rect = play_again_text.get_rect(center=play_again_rect.center)
    quit_text_rect = quit_text.get_rect(center=quit_rect.center)

    clock = pygame.time.Clock()

    # Vòng lặp chờ sự kiện người dùng
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    reset_callback()
                    return
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.blit(overlay, (0, 0))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, (255, 255, 255), play_again_rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), play_again_rect, 2, border_radius=6)
        screen.blit(play_again_text, play_again_text_rect)

        pygame.draw.rect(screen, (255, 255, 255), quit_rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), quit_rect, 2, border_radius=6)
        screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()
        clock.tick(60)
