class Node():
    def __init__(self, state, parent=None):
        self.visits = 1
        self.reward = 0.0
        self.state = state  # Instance of Connect4Game
        self.children = []
        self.children_moves = []
        self.parent = parent

    def add_child(self, child_state, move):
        child = Node(child_state, parent=self)
        self.children.append(child)
        self.children_moves.append(move)

    def update(self, reward):
        self.reward += reward
        self.visits += 1

    def fully_explored(self):
        if len(self.children) == len(self.state.get_valid_locations()):
            return True
        return False
