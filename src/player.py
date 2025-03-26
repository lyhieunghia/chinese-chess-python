class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.is_winner = False
        self.move_history = [] 

    def add_move(self, start_pos, end_pos):
        """
        start_pos: (x,y)
        end_pos: (x,y)
        """
        self.move_history.append((start_pos, end_pos))

    def get_last_move(self):
        return self.move_history[-1] if self.move_history else None

    def reset_moves(self):
        self.move_history.clear()

    def set_winner(self):
        self.is_winner = True

    def get_info(self):
        status = "(Winner)" if self.is_winner else ""
        return f"Player: {self.name}, Color: {self.color} {status}"
