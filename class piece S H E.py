class Piece:
    RED = "red"
    BLACK = "black"

    def __init__(self, x: int, y: int, player: str, piece_type: str):
        self.x = x
        self.y = y
        self.player = player  
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
        return f"{self.piece_type}({self.x}, {self.y}, {self.player})"


class Soldier(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "Soldier")

    def is_valid_move(self, final_x: int, final_y: int, board) -> bool:
        dx = final_x - self.x
        dy = final_y - self.y

        if not (0 <= final_x <= 8 and 0 <= final_y <= 9):  
            return False

        if board.get_piece(final_x, final_y) and board.get_piece(final_x, final_y).player == self.player:
            return False  

        if self.player == self.RED:
            if self.y <= 4:  
                return dx == 0 and dy == 1  
            else:
                return (dx == 0 and dy == 1) or (abs(dx) == 1 and dy == 0)  

        elif self.player == self.BLACK:
            if self.y >= 5:  
                return dx == 0 and dy == -1  
            else:
                return (dx == 0 and dy == -1) or (abs(dx) == 1 and dy == 0)  

        return False


class Horse(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "Horse")

    def is_valid_move(self, final_x: int, final_y: int, board) -> bool:
        dx = abs(final_x - self.x)
        dy = abs(final_y - self.y)

        if not (0 <= final_x <= 8 and 0 <= final_y <= 9):  
            return False

        if board.get_piece(final_x, final_y) and board.get_piece(final_x, final_y).player == self.player:
            return False  

        if (dx, dy) in [(2, 1), (1, 2)]:  
            
            if dx == 2:  
                leg_x = self.x + (final_x - self.x) // 2
                if board.get_piece(leg_x, self.y) is not None:
                    return False
            elif dy == 2:  
                leg_y = self.y + (final_y - self.y) // 2
                if board.get_piece(self.x, leg_y) is not None:
                    return False
            return True
        return False


class Elephant(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "Elephant")

    def is_valid_move(self, final_x: int, final_y: int, board) -> bool:
        dx = abs(final_x - self.x)
        dy = abs(final_y - self.y)

        if not (0 <= final_x <= 8 and 0 <= final_y <= 9):  
            return False

        if board.get_piece(final_x, final_y) and board.get_piece(final_x, final_y).player == self.player:
            return False  

        if (dx, dy) == (2, 2):  
            
            mid_x = (self.x + final_x) // 2
            mid_y = (self.y + final_y) // 2
            if board.get_piece(mid_x, mid_y) is not None:
                return False
            
            if self.player == self.RED and final_y > 4:
                return False
            if self.player == self.BLACK and final_y < 5:
                return False

            return True
        return False