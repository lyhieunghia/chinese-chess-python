class Piece:
    RED = "red"
    BLACK = "black"

    def __init__(self, x: int, y: int, player, piece_type: str):
        self.x = x
        self.y = y
        self.player = player  # Player object
        self.piece_type = piece_type  

    def is_valid_move(self, final_x: int, final_y: int, board) -> bool:
        raise NotImplementedError("This method should be overridden by subclasses.")

    def move(self, final_x: int, final_y: int, board) -> bool:
        if self.is_valid_move(final_x, final_y, board):
            self.x = final_x
            self.y = final_y
            return True
        return False

    def __str__(self):
        return f"{self.piece_type}({self.x}, {self.y}, {self.player.color})"

class Chariot(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "chariot")

    def is_valid_move(self, final_x, final_y, board):
        if final_x != self.x and final_y != self.y:
            return False  # Xe chỉ đi thẳng ngang hoặc dọc
        
        # Kiểm tra có quân cản đường không
        if final_x == self.x:
            step = 1 if final_y > self.y else -1
            for y in range(self.y + step, final_y, step):
                if board.get_piece(self.x, y):
                    return False
        else:
            step = 1 if final_x > self.x else -1
            for x in range(self.x + step, final_x, step):
                if board.get_piece(x, self.y):
                    return False
        
        return True

class Cannon(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "cannon")

    def is_valid_move(self, final_x, final_y, board):
        if final_x != self.x and final_y != self.y:
            return False  # Phao chỉ đi thẳng ngang hoặc dọc
        
        # Đếm số quân cản đường
        count = 0
        if final_x == self.x:
            step = 1 if final_y > self.y else -1
            for y in range(self.y + step, final_y, step):
                if board.get_piece(self.x, y):
                    count += 1
        else:
            step = 1 if final_x > self.x else -1
            for x in range(self.x + step, final_x, step):
                if board.get_piece(x, self.y):
                    count += 1
        
        target_piece = board.get_piece(final_x, final_y)
        if target_piece:
            return count == 1 and target_piece.player.color != self.player.color
        return count == 0

class General(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "general")

    def is_valid_move(self, final_x, final_y, board):
        if not (3 <= final_x <= 5 and (0 <= final_y <= 2 if self.player.color == self.RED else 7 <= final_y <= 9)):
            return False  # Chỉ đi trong cung
        return abs(final_x - self.x) + abs(final_y - self.y) == 1

class Advisor(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "advisor")

    def is_valid_move(self, final_x, final_y, board):
        if not (3 <= final_x <= 5 and (0 <= final_y <= 2 if self.player.color == self.RED else 7 <= final_y <= 9)):
            return False  # Chỉ đi trong cung
        return abs(final_x - self.x) == 1 and abs(final_y - self.y) == 1

class Soldier(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "soldier")

    def is_valid_move(self, final_x: int, final_y: int, board) -> bool:
        if self.player.color == self.RED:
            if self.y <= 4:  # Trước khi qua sông chỉ đi thẳng
                return final_x == self.x and final_y == self.y + 1
            else:
                return (final_x == self.x and final_y == self.y + 1) or (abs(final_x - self.x) == 1 and final_y == self.y)
        else:
            if self.y >= 5:  # Trước khi qua sông chỉ đi thẳng
                return final_x == self.x and final_y == self.y - 1
            else:
                return (final_x == self.x and final_y == self.y - 1) or (abs(final_x - self.x) == 1 and final_y == self.y)

class Horse(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "horse")

    def is_valid_move(self, final_x: int, final_y: int, board) -> bool:
        dx = abs(final_x - self.x)
        dy = abs(final_y - self.y)
        if (dx, dy) not in [(2, 1), (1, 2)]:
            return False
        
        if dx == 2 and board.get_piece((self.x + final_x) // 2, self.y):
            return False
        if dy == 2 and board.get_piece(self.x, (self.y + final_y) // 2):
            return False
        
        return True

class Elephant(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "elephant")

    def is_valid_move(self, final_x: int, final_y: int, board) -> bool:
        dx = abs(final_x - self.x)
        dy = abs(final_y - self.y)
        if (dx, dy) != (2, 2):
            return False
        
        mid_x = (self.x + final_x) // 2
        mid_y = (self.y + final_y) // 2
        if board.get_piece(mid_x, mid_y):
            return False
        
        if self.player.color == self.RED and final_y > 4:
            return False
        if self.player.color == self.BLACK and final_y < 5:
            return False
        
        return True
