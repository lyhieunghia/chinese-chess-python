import pygame
from piece import *

pygame.init()

class BoardGame:
    def __init__(self, game):
        self.game = game
        self.red_pieces = []
        self.black_pieces = []
        self.board_array = [[None for _ in range(9)] for _ in range(10)]
        self.set_pieces()
        self.is_flip = True

        # Thiết lập kích thước ô và vị trí bàn cờ trên màn hình
        self.dot_size = 16
        self.cell_size = 60
        self.piece_icon = 40
        self.piece_size = 52
        self.piece_gap = self.cell_size - self.piece_size
        self.board_width = 9 * self.cell_size
        self.board_height = 10 * self.cell_size
        self.offset_x = 0 #(self.game.width - self.board_width) // 2
        self.offset_y = 0 #(self.game.height - self.board_height) // 2

        # Load ảnh bàn cờ và quân cờ
        self.BLACK_COLOR = (0, 0, 0)
        self.PIECE_COLOR = (222, 184, 135)
        self.SELECTED_COLOR = (159, 0, 255)
        self.CHECK_COLOR = (255, 92, 0)

        self.board_image = pygame.image.load("./assets/images/brown_board.jpg").convert()
        self.board_image = pygame.transform.scale(self.board_image, (self.board_width, self.board_height))

        self.piece_images = {
            name: pygame.image.load(path).convert_alpha()
            for name, path in {
                "general_black": "./assets/images/black/general_black.png",
                "advisor_black": "./assets/images/black/minister_black.png",
                "elephant_black": "./assets/images/black/elephant_black.png",
                "chariot_black": "./assets/images/black/chariot_black.png",
                "horse_black": "./assets/images/black/horse_black.png",
                "cannon_black": "./assets/images/black/cannon_black.png",
                "soldier_black": "./assets/images/black/soldier_black.png",

                "general_red": "./assets/images/red/general_red.png",
                "advisor_red": "./assets/images/red/minister_red.png",
                "elephant_red": "./assets/images/red/elephant_red.png",
                "chariot_red": "./assets/images/red/chariot_red.png",
                "horse_red": "./assets/images/red/horse_red.png",
                "cannon_red": "./assets/images/red/cannon_red.png",
                "soldier_red": "./assets/images/red/soldier_red.png"
            }.items()
        }

        #Biến kéo thả
        self.selected_piece: Piece = None
        self.dragging_piece = None
        self.drag_offset = (0,0)

        #Âm thanh
        self.move_sound = pygame.mixer.Sound("./assets/sounds/move.mp3")
        self.capture_sound = pygame.mixer.Sound("./assets/sounds/capture.mp3")
        self.start_sound = pygame.mixer.Sound("./assets/sounds/game_start.mp3")
        self.end_sound = pygame.mixer.Sound("./assets/sounds/game_end.mp3")
        self.check_sound = pygame.mixer.Sound("./assets/sounds/check.mp3")
        self.illegal = pygame.mixer.Sound("./assets/sounds/illegal.mp3")
        

    def set_pieces(self):
        """Khởi tạo quân cờ ban đầu cho cả 2 người chơi."""
        self.set_player_pieces(self.game.player1)
        self.set_player_pieces(self.game.player2)
        self.set_piece_vectors()

    def set_player_pieces(self, player):
        if player.color == "black":
            self.set_black_pieces(player)
        else:
            self.set_red_pieces(player)

    def set_black_pieces(self, black_player):
        self.black_pieces.append(Chariot(9, 0, black_player))
        self.black_pieces.append(Chariot(9, 8, black_player))

        self.black_pieces.append(Horse(9, 1, black_player))
        self.black_pieces.append(Horse(9, 7, black_player))

        self.black_pieces.append(Elephant(9, 2, black_player))
        self.black_pieces.append(Elephant(9, 6, black_player))

        self.black_pieces.append(Advisor(9, 3, black_player))
        self.black_pieces.append(Advisor(9, 5, black_player))

        self.black_pieces.append(General(9, 4, black_player))

        self.black_pieces.append(Cannon(7, 1, black_player))
        self.black_pieces.append(Cannon(7, 7, black_player))

        for i in range(0, 9, 2):
            self.black_pieces.append(Soldier(6, i, black_player))

    def set_red_pieces(self, red_player):
        self.red_pieces.append(Chariot(0, 0, red_player))
        self.red_pieces.append(Chariot(0, 8, red_player))

        self.red_pieces.append(Horse(0, 1, red_player))
        self.red_pieces.append(Horse(0, 7, red_player))

        self.red_pieces.append(Elephant(0, 2, red_player))
        self.red_pieces.append(Elephant(0, 6, red_player))

        self.red_pieces.append(Advisor(0, 3, red_player))
        self.red_pieces.append(Advisor(0, 5, red_player))

        self.red_pieces.append(General(0, 4, red_player))

        self.red_pieces.append(Cannon(2, 1, red_player))
        self.red_pieces.append(Cannon(2, 7, red_player))

        for i in range(0, 9, 2):
            self.red_pieces.append(Soldier(3, i, red_player))

    def set_piece_vectors(self):
        """Cập nhật vị trí các quân cờ vào ma trận bàn cờ."""
        self.board_array = [[None for _ in range(9)] for _ in range(10)]
        for piece in self.red_pieces:
            self.board_array[piece.x][piece.y] = piece
        for piece in self.black_pieces:
            self.board_array[piece.x][piece.y] = piece

    def get_board_pos(self, pos):
        """Chuyển đổi tọa độ pixel sang vị trí bàn cờ (hàng, cột)."""
        col = (pos[0] - self.offset_x) // self.cell_size
        row = (pos[1] - self.offset_y) // self.cell_size
        if self.is_flip:
            col = 8 - col
            row = 9 - row
        return (row, col) if 0 <= row < 10 and 0 <= col < 9 else None

    def get_piece(self, row, col):
        """Trả về quân cờ tại vị trí (x, y) nếu có."""
        return self.board_array[row][col] if 0 <= row < 10 and 0 <= col < 9 else None
    
    # hàm này để trả về chuỗi các nước đi hợp lệ của quân cờ được chọn
    def get_all_possible_moves(self, piece):
        moves = []
        for row in range(10):
            for col in range(9):
                if piece.is_valid_move(row, col, self):
                    moves.append((row, col))
        return moves

    
    # hàm trả về quân tướng theo màu
    def find_general(self, color):
        for row in range(10):
            for col in range(9):
                piece = self.get_piece(row, col)
                if piece and piece.piece_type == "general" and piece.player.color == color:
                    return piece
        return None  # Không tìm thấy tướng (có thể đã bị bắt)

    # hàm này kiểm tra trường hợp nếu hai tướng đối mặt nhau
    # hàm chỉ kiểm tra sau khi di chuyển!
    def generals_face_each_other(self, color):
        # lấy tướng theo màu
        my_general = self.find_general(color)

        # tìm màu của đối thủ
        opponent_color = 'red' if color == 'black' else 'black'
        # lấy tướng bên đối thủ
        opponent_general = self.find_general(opponent_color)

        # Nếu một trong hai tướng đã mất => game kết thúc 
        if not my_general or not opponent_general:
            return False

        # Nếu cùng cột mà có hai tướng
        if my_general.y == opponent_general.y:
            # Kiểm tra xem có quân cờ nào nằm giữa không
            # lấy cột chứa hai tướng và chạy kiểm tra các hàng
            col = my_general.y

            start_row = min(my_general.x, opponent_general.x) + 1
            end_row = max(my_general.x, opponent_general.x)

            for row in range(start_row, end_row):
                # nếu tại vị trí đấy có quân thì chưa bị chiếu
                if self.get_piece(row, col) is not None:
                    return False  # Có quân cờ chắn giữa

            return True  # Không có quân cờ chắn, tướng đối mặt
        # nếu không gặp trường hợp đối mặt tướng
        return False

    def move_piece(self, piece, final_x, final_y):
        """Di chuyển quân cờ, xử lý ăn quân nếu có và cập nhật bàn cờ."""
        if piece and piece.player == self.game.turn:
            if piece.is_valid_move(final_x, final_y, self):
                if self.is_legal_move(piece, final_x, final_y):
                    target_piece = self.get_piece(final_x, final_y)
                    if target_piece and target_piece.player.color != piece.player.color:
                        self.remove_piece(target_piece)
                        self.capture_sound.play()
                    else:
                        self.move_sound.play()
                    # Xóa quân cờ khỏi vị trí cũ và cập nhật vị trí mới
                    self.board_array[piece.x][piece.y] = None
                    piece.move(final_x, final_y, self)
                    self.board_array[final_x][final_y] = piece
                    return True
                return False
        return False

    def remove_piece(self, piece):
        """Loại bỏ quân cờ bị ăn khỏi danh sách quân cờ."""
        if piece in self.red_pieces:
            self.red_pieces.remove(piece)
        elif piece in self.black_pieces:
            self.black_pieces.remove(piece)


    # hàm sẽ kiểm tra có quân nào bên đối thủ có khả năng ăn quân tướng đang xét
    # bao gồm cả trường hợp tướng đối mặt
    def is_in_check(self, color):
        # tìm quân tướng trong bàn cờ theo màu
        general = self.find_general(color)

        # nếu không tìm thấy thì ngưng hàm(general có thể = None)
        if not general:
            return False
        
        # kiểm tra trường hợp đối mặt tướng
        if self.generals_face_each_other(color):
            return True
        
        # lưu vị trí của quân tướng để kiểm tra
        general_pos = (general.x, general.y)

        # lấy danh sách quân cờ của bên đối thủ
        # trả về danh sách đen nếu bên kiểm tra là đỏ và ngược lại
        opponent_color = 'black' if color == 'red' else 'red'
        opponent_pieces = []
        for row in range(9):
            for col in range(10):
                piece = self.get_piece(row, col)
                if piece and piece.player.color == opponent_color:
                    opponent_pieces.append(piece)
                

        # chạy danh sách và kiểm tra nếu có quân đối thủ chiếu được
        for piece in opponent_pieces:
            # self ở đây là BoardGame
            if piece.is_valid_move(general_pos[0], general_pos[1], self):
                return True
        
        # nếu không bị chiếu
        return False


    def is_checkmate(self, player):
        if player.color == "red":
            own_pieces = self.red_pieces
        else:
            own_pieces = self.black_pieces

        # Nếu không bị chiếu thì không phải chiếu bí
        if not self.is_in_check(player.color):
            return False

        # Thử mọi nước đi có thể với mọi quân, 
        # nếu có nước nào thoát khỏi chiếu thì không phải chiếu bí
        for piece in own_pieces:
            possible_moves = self.get_all_possible_moves(piece)
            for move in possible_moves:
                original_pos = (piece.x, piece.y)
                # gọi *move vì các phần tử trong possible_moves là tuple => gọi [0] và [1]
                target_piece = self.get_piece(*move)

                # Tạm thời di chuyển quân
                self.board_array[piece.x][piece.y] = None
                piece.x, piece.y = move
                captured = None
                if target_piece:
                    self.remove_piece(target_piece)
                    captured = target_piece
                self.board_array[move[0]][move[1]] = piece

                # Kiểm tra sau khi di chuyển có còn bị chiếu không
                still_in_check = self.is_in_check(player.color)

                # Hoàn tác di chuyển
                self.board_array[move[0]][move[1]] = captured if captured else None
                piece.x, piece.y = original_pos
                self.board_array[original_pos[0]][original_pos[1]] = piece
                if captured:
                    if captured.player.color == "red":
                        self.red_pieces.append(captured)
                    else:
                        self.black_pieces.append(captured)

                # Nếu có ít nhất 1 nước đi khiến không còn bị chiếu
                if not still_in_check:
                    return False

        # Không có nước nào giúp thoát chiếu
        return True

    # hàm này để kiểm tra xem nước đi có để hổng quân tướng không
    # hàm này sẽ kết hợp cùng is_valid_move(...)
    def is_legal_move(self, piece: Piece, to_row: int, to_col: int):
        # Giả lập nước đi của một quân cờ, 
        # kiểm tra xem nước đi đó có khiến tướng bị chiếu không

        # vị trí ban đầu của quân cờ
        origin_row, origin_col = piece.x, piece.y
        # lấy quân cờ tại vị trí được giả lập để di chuyển tới
        captured_piece = self.get_piece(to_row, to_col)


        # Tạm thời di chuyển quân đến vị trí muốn thử nghiệm
        self.board_array[to_row][to_col] = piece
        # Tạm thời xóa uân tại vị trí cũ
        self.board_array[origin_row][origin_col] = None
        # Cập nhật tọa độ mới cho quân cờ được giả lập
        piece.x, piece.y = to_row, to_col

        # Kiểm tra sau khi di chuyển thì tướng có bị chiếu không.
        # hàm này trả về True nếu có bị chiếu và False nếu không
        in_check = self.is_in_check(self.game.turn.color)

        # Hoàn tác di chuyển
        self.board_array[origin_row][origin_col] = piece
        self.board_array[to_row][to_col] = captured_piece
        piece.x, piece.y = origin_row, origin_col

        # trả về not... vì như chú thích ở trên, khi trả về False nghĩa là không bị chiếu
        # nên đảo ngược lại thành True từ hàm is_legal_move là nước đi có hợp lệ
        return not in_check
    
    
    """
    def is_checkmate(self, player):
        #Kiểm tra nếu tướng của người chơi bị chiếu bí (có quân đối phương có thể di chuyển tới vị trí của tướng).
        general = None
        if player.color == "red":
            pieces = self.red_pieces
            enemy = self.black_pieces
        else:
            pieces = self.black_pieces
            enemy = self.red_pieces
        for piece in pieces:
            if isinstance(piece, General):
                general = piece
                break
        if general:
            for enemy_piece in enemy:
                if enemy_piece.is_valid_move(general.x, general.y, self):
                    return True
        return False
        """

    def draw(self):
        self.draw_board()
        self.draw_pieces()

        if self.selected_piece:
            self.highlight_possible_move(self.selected_piece)

        highlight_piece = self.dragging_piece or self.selected_piece
        if highlight_piece:
            self.draw_piece(highlight_piece, True)


    def draw_board(self):
        """Vẽ ảnh bàn cờ lên màn hình tại vị trí đã tính toán."""
        self.draw_board_background()
        self.draw_board_lines()

    def draw_board_background(self):
        # Tạo surface có viền bo tròn
        rounded_surface = pygame.Surface((self.board_width, self.board_height), pygame.SRCALPHA)
        pygame.draw.rect(rounded_surface, (255, 255, 255, 0), rounded_surface.get_rect(), border_radius=30)
        rounded_surface.blit(self.board_image, (0, 0))

        # Vẽ surface lên màn hình chính
        self.game.screen.blit(rounded_surface, (self.offset_x, self.offset_y))

    def draw_board_lines(self):
        left = self.offset_x + self.cell_size // 2
        top = self.offset_y + self.cell_size // 2
        right = left + 8 * self.cell_size
        bottom = top + 9 * self.cell_size

        # 10 hàng ngang
        for row in range(10):
            y = top + row * self.cell_size
            pygame.draw.line(self.game.screen, self.BLACK_COLOR, (left, y), (right, y), 2)

        # 9 cột dọc (chừa sông)
        for col in range(9):
            x = left + col * self.cell_size
            pygame.draw.line(self.game.screen, self.BLACK_COLOR, (x, top), (x, top + 4 * self.cell_size), 2)
            pygame.draw.line(self.game.screen, self.BLACK_COLOR, (x, top + 5 * self.cell_size), (x, bottom), 2)

            # Đường chéo cung tướng
            def draw_palace(x_start, y_start):
                pygame.draw.line(self.game.screen, self.BLACK_COLOR,
                    (x_start + 3 * self.cell_size, y_start),
                    (x_start + 5 * self.cell_size, y_start + 2 * self.cell_size), 2)
                pygame.draw.line(self.game.screen, self.BLACK_COLOR,
                    (x_start + 5 * self.cell_size, y_start),
                    (x_start + 3 * self.cell_size, y_start + 2 * self.cell_size), 2)

        draw_palace(left, top)
        draw_palace(left, top + 7 * self.cell_size)

    def draw_pieces(self):
        """Vẽ tất cả quân cờ lên bàn cờ."""
        for row in range(10):
            for col in range(9):
                piece = self.board_array[row][col]
                if piece and piece != self.dragging_piece:
                    #self.draw_piece(piece, False)
                    # kiểm tra xem quân đang xét có phải tướng không, nếu là tướng
                    # thì có bị chiếu không?
                    is_check = (
                    piece.piece_type == "general"
                    and piece.player == self.game.turn
                    and self.is_in_check(piece.player.color)
                    )
                    self.draw_piece(piece, False, is_check)


    # tham số is_check để kiểm tra và tô viền cho quân tướng nếu bị chiếu
    def draw_piece(self, piece, is_highlight, is_check = False):
        """Vẽ một quân cờ tại vị trí của nó."""
        if self.dragging_piece == piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x = mouse_x - self.drag_offset[0]
            y = mouse_y - self.drag_offset[1]
        else:
            col = 8 - piece.y if self.is_flip else piece.y
            row = 9 - piece.x if self.is_flip else piece.x

            x = self.offset_x + col * self.cell_size + (self.cell_size - self.piece_size) // 2
            y = self.offset_y + row * self.cell_size + (self.cell_size - self.piece_size) // 2

        piece_image = self.piece_images.get(f"{piece.piece_type}_{piece.player.color}")
        if piece_image:
            surface = self.create_piece_surface(piece_image, piece.player.color, is_highlight, is_check)
            self.game.screen.blit(surface, (x, y))

    # tham số is_check như trên
    def create_piece_surface(self, original_image, color, is_selected : bool, is_check: bool = False):
        """Tạo surface tròn với viền và ảnh quân cờ ở giữa."""
        surface = pygame.Surface((self.piece_size, self.piece_size), pygame.SRCALPHA)
        center = self.piece_size // 2

        # Vẽ nền tròn
        bg_color = self.SELECTED_COLOR if is_selected else self.PIECE_COLOR
        pygame.draw.circle(surface, bg_color, (center, center), center)

        # Viền đen ngoài
        if is_check:
            pygame.draw.circle(surface, self.CHECK_COLOR, (center, center), center, 4)
        else:
            pygame.draw.circle(surface, self.BLACK_COLOR, (center, center), center, 2)

        # Vẽ icon đã resize vào giữa
        resized_icon = pygame.transform.smoothscale(original_image, (self.piece_icon, self.piece_icon))
        offset = (self.piece_size - self.piece_icon) // 2
        surface.blit(resized_icon, (offset, offset))

        
        # Vẽ viền nhỏ ở trong
        border_color = (169, 21, 21) if color == "red" else (0, 0, 0)
        border_width = 2

        pygame.draw.circle(surface, border_color, (center, center), self.piece_icon // 2, border_width)
        return surface
    
    
    def highlight_possible_move(self, piece: Piece):
        for row in range(10):
            for col in range(9):
                # kiểm tra nước đi có thể đi
                if piece.is_valid_move(row, col, self):
                    # kiểm tra tính hợp lệ của nước đi đó
                    if self.is_legal_move(piece, row, col):
                        target = self.get_piece(row, col)
                        if target and target.player.color != piece.player.color:
                            self.draw_piece(target, True)
                        else:
                            self.draw_highlight_dot(row, col)


    def draw_highlight_dot(self, row, col):
        row = 9 - row if self.is_flip else row
        col = 8 - col if self.is_flip else col

        x = self.offset_x + col * self.cell_size + self.cell_size // 2
        y = self.offset_y + row * self.cell_size + self.cell_size // 2

        surface = pygame.Surface((self.dot_size, self.dot_size), pygame.SRCALPHA)
        center = self.dot_size // 2
        pygame.draw.circle(surface, self.SELECTED_COLOR, (center, center), center)
        self.game.screen.blit(surface, (x - center, y - center))

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(event)


    def handle_mouse_down(self, event):
        if event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            board_pos = self.get_board_pos(mouse_pos)
            if board_pos:
                row, col = board_pos
                piece = self.get_piece(row, col)

                if piece and piece.player == self.game.turn:
                    self.selected_piece = piece
                    self.dragging_piece = piece

                    row = 9 - piece.x if self.is_flip else piece.x
                    col = 8 - piece.y if self.is_flip else piece.y
                    px = self.offset_x + col * self.cell_size
                    py = self.offset_y + row * self.cell_size
                    self.drag_offset = (mouse_pos[0] - px, mouse_pos[1] - py)

    def handle_mouse_up(self, event):
        if event.button  == 1:
            if self.dragging_piece or self.selected_piece:
                mouse_pos = pygame.mouse.get_pos()
                board_pos = self.get_board_pos(mouse_pos)

                if board_pos:
                    row, col = board_pos
                    moved = self.move_piece(self.selected_piece, row, col)

                    if moved:
                        self.game.switch_turn()
                        self.selected_piece = None

                        if self.is_in_check(self.find_general(self.game.get_opponent().color)):
                            self.check_sound.play()
                    elif (row, col) != (self.selected_piece.x, self.selected_piece.y):
                        self.illegal.play()
        
        self.drag_offset = (0, 0)
        self.dragging_piece = None

    def reset_game(self):
        """Đặt lại toàn bộ bàn cờ và quân cờ như lúc bắt đầu trò chơi."""
        # Xóa dữ liệu cũ
        self.red_pieces.clear()
        self.black_pieces.clear()
        self.board_array = [[None for _ in range(9)] for _ in range(10)]
        
        # Xóa quân cờ đang chọn vì nếu có quân được chọn khi nhấn reset thì quân đó
        # sẽ không bị làm mới theo bàn cờ => trở thành quân cờ ma
        self.selected_piece = None

        # Thiết lập lại các quân cờ
        self.set_pieces()

        # mặc định bên đỏ đi trước(mấy thuộc tính này nằm bên game)
        self.game.turn = self.game.player1
        self.game.gameover = False
        self.start_sound.play()

    def flip_board(self):
        self.is_flip = False if self.is_flip else True
