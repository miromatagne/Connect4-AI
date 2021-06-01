"""
    This class is used to represent nodes of the tree of boards used during
    Monte-Carlo Tree Search.
"""


class Node():
    def __init__(self, state, parent=None):
        self.visits = 1
        self.reward = 0.0
        self.state = state  # Instance of Connect4Game
        self.children = []
        self.children_moves = []
        self.parent = parent

    def add_child(self, child_state, move):
        """
            Add a child to the current node.

            :param child_state: state of the child to add
            :param move: move to do to get to the newly added child
        """
        child = Node(child_state, parent=self)
        self.children.append(child)
        self.children_moves.append(move)

    def update(self, reward):
        """
            Update the node's reward (indicates how good a certain node is 
            according to the MCTS algorithm)

            :param reward: reward to be added to the node
        """
        self.reward += reward
        self.visits += 1

    def fully_explored(self):
        """
            Checks if the node is fully explored (which means we can not add
            any more children to this node)

            :return: True of False depending on if it is fully epxlored or not
        """
        if len(self.children) == len(self.state.get_valid_locations()):
            return True
        return False
