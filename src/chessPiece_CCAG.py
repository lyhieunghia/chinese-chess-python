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

#board tinh theo (x, y) voi x nam ngang va y nam doc
# co gia tri: 0 <= x <= 8
#             0 <= y <= 9

# xe
class Chariot(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "Chariot")

    def is_valid_move(self, final_x, final_y, board):
        #final x/y la vi tri moi cua quan co
        dx = final_x - self.x
        dy = final_y - self.y

        # neu quan co khong nam trong ban co
        if not (0 <= final_x <= 8 and 0 <= final_y <= 9):  
            return False
        
        # xu ly khi vi tri di chuyen toi co quan co dong minh? 
        if board.get_piece(final_x, final_y) and board.get_piece(final_x, final_y).player == self.player:
            return False 
        
        # di chuyen
        # xe do
        if self.player == self.RED:
            # quan xe di theo truc doc va ngang nen chi can kiem tra toa do cua x hoac y
            # TH1: di thang theo truc y(ngang) -> chi co gia tri y thay doi
            if(final_x == self.x and final_y != self.y):
                return True
            # TH2: di doc 
            elif(final_x != self.x and final_y == self.y):
                return True
            # TH3: neu ca hai toa do deu thay doi -> khong hop le
            else:
                return False
            
        # xe xanh
        if self.player == self.BLACK:
            # quan xe di theo truc doc va ngang nen chi can kiem tra toa do cua x hoac y
            # TH1: di thang theo truc y(ngang) -> chi co gia tri y thay doi
            if(final_x == self.x and final_y != self.y):
                return True
            # TH2: di doc 
            elif(final_x != self.x and final_y == self.y):
                return True
            # TH3: neu ca hai toa do deu thay doi -> khong hop le
            else:
                return False
            
# phao
class Canon(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "Canon")

    def is_valid_move(self, final_x, final_y, board):
        #final x/y la vi tri moi cua quan co
        dx = final_x - self.x
        dy = final_y - self.y

        # neu quan co khong nam trong ban co
        if not (0 <= final_x <= 8 and 0 <= final_y <= 9):  
            return False
        
        # xu ly khi vi tri di chuyen toi co quan co dong minh? 
        if board.get_piece(final_x, final_y) and board.get_piece(final_x, final_y).player == self.player:
            return False 
        
        # di chuyen
        # phao do
        if self.player == self.RED:
            # quan phao di theo truc doc va ngang nen chi can kiem tra toa do cua x hoac y
            # TH1: di thang theo truc y(ngang) -> chi co gia tri y thay doi
            if(final_x == self.x and final_y != self.y):
                return True
            # TH2: di doc 
            elif(final_x != self.x and final_y == self.y):
                return True
            # TH3: neu ca hai toa do deu thay doi -> khong hop le
            else:
                return False
            
        # di chuyen
        # phao xanh
        if self.player == self.RED:
            # quan phao di theo truc doc va ngang nen chi can kiem tra toa do cua x hoac y
            # TH1: di thang theo truc y(ngang) -> chi co gia tri y thay doi
            if(final_x == self.x and final_y != self.y):
                return True
            # TH2: di doc 
            elif(final_x != self.x and final_y == self.y):
                return True
            # TH3: neu ca hai toa do deu thay doi -> khong hop le
            else:
                return False
            
        # chua co truong hop an quan cho phao!!!!

# tuong
class General(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "General")

    def is_valid_move(self, final_x, final_y, board):
        #final x/y la vi tri moi cua quan co
        dx = abs(final_x - self.x)
        dy = abs(final_y - self.y)

        # neu quan co khong nam trong ban co
        if not (0 <= final_x <= 8 and 0 <= final_y <= 9):  
            return False
        
        # xu ly khi vi tri di chuyen toi co quan co dong minh? 
        if board.get_piece(final_x, final_y) and board.get_piece(final_x, final_y).player == self.player:
            return False 
        
        # di chuyen
        # quan tuong di theo truc doc va ngang nen chi can kiem tra toa do cua x hoac y
        # nhung bi gioi han trong cung nen gioi han cac gia tri x, y:
        # 3 <= x <= 5 
        # 0 <= y <= 2
        # tuong chi di chuyen 1 o nen dx hoac dy phai bang 1

        #kiem tra nuoc di trong gioi han trong cung thanh
        if((3 <= final_x and final_x <= 5) and (0 <= final_y and final_y <= 2)):
            return False

        #kiem tra do dai hop le
        #hai dieu kien () or () khong the cung xay ra
        if((dx == 1 and dy == 0) or (dx == 0 and dy == 1)):
            # tuong do
            if self.player == self.RED:
                # TH1: di thang theo truc y(ngang) -> chi co gia tri y thay doi
                if(final_x == self.x and final_y != self.y):
                    return True
                # TH2: di doc 
                elif(final_x != self.x and final_y == self.y):
                    return True
                # TH3: neu ca hai toa do deu thay doi -> khong hop le
                else:
                    return False
            
            # di chuyen
            # tuong xanh
            if self.player == self.RED:
                # quan tuong di theo truc doc va ngang nen chi can kiem tra toa do cua x hoac y
                # TH1: di thang theo truc y(ngang) -> chi co gia tri y thay doi
                if(final_x == self.x and final_y != self.y):
                    return True
                # TH2: di doc 
                elif(final_x != self.x and final_y == self.y):
                    return True
                # TH3: neu ca hai toa do deu thay doi -> khong hop le
                else:
                    return False

# si
class Advisor(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player, "Advisor")

    def is_valid_move(self, final_x, final_y, board):
        #final x/y la vi tri moi cua quan co
        dx = abs(final_x - self.x)
        dy = abs(final_y - self.y)

        # neu quan co khong nam trong ban co
        if not (0 <= final_x <= 8 and 0 <= final_y <= 9):  
            return False
        
        # xu ly khi vi tri di chuyen toi co quan co dong minh? 
        if board.get_piece(final_x, final_y) and board.get_piece(final_x, final_y).player == self.player:
            return False 
        
        # di chuyen
        # quan si di cheo -> di chuyen theo ca truc x(ngang) va y(doc) 
        # nhung bi gioi han trong cung nen gioi han cac gia tri x, y:
        # 3 <= x <= 5 
        # 0 <= y <= 2
        # => dx a dy phai bang nhau va bang 1: dx = dy = 1

        #kiem tra nuoc di trong gioi han trong cung thanh
        if((3 <= final_x and final_x <= 5) and (0 <= final_y and final_y <= 2)):
            return False

        # Kiem tra vi tri co hop le?
        if(dx == dy == 1):

            # di chuyen
            # si do
            if self.player == self.RED:
                return True
            # di chuyen
            # si xanh
            if self.player == self.RED:
                return True
        else:
            return False    