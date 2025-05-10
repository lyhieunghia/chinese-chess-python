#################!!!##################
#           LƯU Ý
# 1. GỐC TỌA ĐỘ BÀN CỜ NẰM Ở BÊN GSC TRÁI 
# PHÍA TRÊN.
# 2.TRỤC X NẰM DỌC, TRỤC Y NẰM NGANG
#################!!!##################

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

# XE
class Chariot(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "chariot")

    def is_valid_move(self, final_x, final_y, board):
        if final_x != self.x and final_y != self.y:
            return False  # Xe chỉ đi thẳng ngang hoặc dọc
        
        # Kiểm tra có quân cản đường không trên hướng đi không
        # đi thẳng
        if final_x == self.x:
            step = 1 if final_y > self.y else -1
            for y in range(self.y + step, final_y, step):
                if board.get_piece(self.x, y):
                    return False
        # đi ngang        
        else:
            step = 1 if final_x > self.x else -1
            for x in range(self.x + step, final_x, step):
                if board.get_piece(x, self.y):
                    return False
        
        #return True
        target_piece = board.get_piece(final_x, final_y)
        # nếu mà điểm đícch có tồn tại quân cờ
        if target_piece:
            # nếu quân đó khác màu thì True ngược lại thì False
            return target_piece.player.color != self.player.color
        # nếu không tồn tại
        else:
            return True
        
# PHÁO
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

# TƯỚNG
class General(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "general")

    def is_valid_move(self, final_x, final_y, board):
        if not (3 <= final_y <= 5 and (0 <= final_x <= 2 if self.player.color == self.RED else 7 <= final_x <= 9)):
            return False  # Chỉ đi trong cung
        
        # kiểm tra delta(x, y): giá trị thay đổi của biến (x, y) 
        # giữa self(x, y) và final(x, y)
        delta_x = abs(final_x - self.x)
        delta_y = abs(final_y - self.y)

        # Kiểm tra đi chéo nếu ở trung tâm cung
        # center_x = 1 if self.player.color == self.RED else 8
        # center_y = 4

        # kiểm tra xem điểm đích có quân cờ không
        target_piece = board.get_piece(final_x, final_y)
        
        # # tướng sẽ có thêm khả năng đi chéo khi ở trung tâm
        # # nếu tướng đỏ hoặc đen ở trung tâm
        # if(self.x == center_x and self.y == center_y):
        #    # kiểm tra xem nếu delta_x/y == 1
        #     if(delta_x == 1 and delta_y == 1):
        #         # nếu mà điểm đích có tồn tại quân cờ
        #         if target_piece:
        #         # nếu quân đó khác màu thì True ngược lại thì False
        #             return target_piece.player.color != self.player.color
        #         # nếu không tồn tại
        #         else:
        #             return True
            # không đặt dòng này vì tướng vẫn có thể đi thẳng, dọc khi đứng ở trung tâm
            # và để cho xét tiếp điều kiên if() ở dưới
            # nếu sai giá trị delta
            # else:
            #    return False  

        # Kiểm tra đi ngang hoặc dọc 1 bước
        if (delta_x == 1 and delta_y == 0) or (delta_x == 0 and delta_y == 1):
            # 1.nếu không có quân cờ ở đích đến thì đi
            # 2.nếu có quân cờ thì chỉ đi khi nó khác màu(bắt quân)
            #  cách này là viết gọn của cách phía trên
            return (not target_piece) or target_piece.player.color != self.player.color

        return False          

# SĨ
class Advisor(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "advisor")

    def is_valid_move(self, final_x, final_y, board):
        if not (3 <= final_y <= 5 and (0 <= final_x <= 2 if self.player.color == self.RED else 7 <= final_x <= 9)):
            return False  # Chỉ đi trong cung
        
        # kiểm tra delta(x, y): giá trị thay đổi của biến (x, y) 
        # giữa self(x, y) và final(x, y)
        delta_x = abs(final_x - self.x)
        delta_y = abs(final_y - self.y)

        # kiểm tra xem nếu delta_x/y == 1
        if(delta_x == 1 and delta_y == 1):
            # kiểm tra xem điểm đích có quân cờ không
            target_piece = board.get_piece(final_x, final_y)

            # nếu mà điểm đích có tồn tại quân cờ
            if target_piece:
                # nếu quân đó khác màu thì True ngược lại thì False
                return target_piece.player.color != self.player.color
            # nếu không tồn tại
            else:
                return True
        # nếu sai giá trị delta
        else:
            return False

        #return abs(final_x - self.x) == 1 and abs(final_y - self.y) == 1

# TỐT
class Soldier(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "soldier")

    def is_valid_move(self, final_x: int, final_y: int, board) -> bool:
        # Kiểm tra cùng màu
        target_piece = board.get_piece(final_x, final_y)
        if target_piece and target_piece.player.color == self.player.color:
            return False

        if self.player.color == self.RED:
            if self.x <= 4:  # Trước khi qua sông chỉ đi thẳng
                return final_x == self.x + 1 and final_y == self.y
            else:  # Sau khi qua sông có thể đi ngang
                return (final_x == self.x + 1 and final_y == self.y) or \
                       (final_x == self.x and abs(final_y - self.y) == 1)
        else:
            if self.x >= 5:  # Trước khi qua sông chỉ đi thẳng
                return final_x == self.x - 1 and final_y == self.y
            else:
                return (final_x == self.x - 1 and final_y == self.y) or \
                       (final_x == self.x and abs(final_y - self.y) == 1)
# MÃ
class Horse(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "horse")

    def is_valid_move(self, final_x: int, final_y: int, board) -> bool:
        dx = abs(final_x - self.x)
        dy = abs(final_y - self.y)

        # Kiểu di chuyển hợp lệ
        if (dx, dy) not in [(2, 1), (1, 2)]:
            return False

        # Kiểm tra cản chân (chân ngựa)
        if dx == 2 and board.get_piece((self.x + final_x) // 2, self.y):
            return False
        if dy == 2 and board.get_piece(self.x, (self.y + final_y) // 2):
            return False

        # Kiểm tra quân cùng màu
        target_piece = board.get_piece(final_x, final_y)
        if target_piece and target_piece.player.color == self.player.color:
            return False

        return True
# TƯỢNG
class Elephant(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "elephant")

    def is_valid_move(self, final_x: int, final_y: int, board) -> bool:
        dx = abs(final_x - self.x)
        dy = abs(final_y - self.y)

        # Di chuyển đúng kiểu 2x2
        if (dx, dy) != (2, 2):
            return False

        # Không được vượt sông
        if self.player.color == self.RED and final_x > 4:
            return False
        if self.player.color == self.BLACK and final_x < 5:
            return False

        # Không có quân chắn giữa
        mid_x = (self.x + final_x) // 2
        mid_y = (self.y + final_y) // 2
        if board.get_piece(mid_x, mid_y):
            return False

        # Kiểm tra quân cùng màu tại đích
        target_piece = board.get_piece(final_x, final_y)
        if target_piece and target_piece.player.color == self.player.color:
            return False

        return True
