from bot import Bot
import random
import math

MONTE_CARLO = "MONTE_CARLO"


class MonteCarlo(Bot):
    def __init__(self, game):
        super().__init__(game, bot_type=MONTE_CARLO)

    def monte_carlo_tree_search(self, iterations, root, factor):
        """
            Main function of MCTS
        """
        for i in range(iterations):
            front, turn = self.tree_policy(root, 1, factor)
            # print(turn)
            reward = self.default_policy(front.state, turn)
            #print("reward:", reward)
            self.backup(front, reward, turn)

        ans = self.best_child(root, 0)
        #print("ANS:", ans.state.last_move[1])
        #print([(c.reward/c.visits) for c in ans.parent.children])
        #print([c.reward for c in ans.parent.children])
        return ans.state.last_move[0]

    def tree_policy(self, node, turn, factor):
        """
            Expands the root node and takes the best child everytime until we reach a winning
            state.
        """
        #turn = node.state._turn
        a = 0
        while not node.state.last_move or not node.state.check_win(node.state.last_move):
            if not node.fully_explored():
                #print("FULLY EXPLORED")
                return self.expand(node, turn), -turn
            else:
                # print(a)
                node = self.best_child(node, factor)
                # print(node.state.last_move)
                b = node.state.check_win(node.state.last_move)
                # print(node.state._board)
                turn *= -1
                # if not b:
                #     exit(2)
                #print("TURN2:", turn)
            a += 1

        return node, turn

    def expand(self, node, turn):
        """
            Add a child state to the node
        """
        tried_children_move = [m for m in node.children_move]
        free_cols = node.state.get_valid_locations()

        for col in free_cols:
            if col not in tried_children_move:
                new_state = node.state.copy_state()
                # print(node.state._board)
                new_state.place(col)
                # print(node.state._board)
                # print(new_state._board)
                #new_state.last_move = [col]
                break

        node.add_child(new_state, col)
        return node.children[-1]

    def backup(self, node, reward, turn):
        #print("turn", turn)
        while node != None:
            node.visits += 1
            node.reward -= turn*reward
            #print("node reward", node.reward)
            node = node.parent
            turn *= -1
        return

    def default_policy(self, state_a, turn):
        """
            Simulates random moves until the game is won by someone and returns a
            reward.
        """
        state = state_a.copy_state()
        while not state.last_move or not state.check_win(state.last_move):
            free_cols = state.get_valid_locations()
            col = random.choice(free_cols)
            state.place(col)
            turn *= -1

        reward_bool = state.check_win(state.last_move)
        if reward_bool and turn == -1:
            reward = 1
        elif reward_bool and turn == 1:
            reward = -1
        else:
            # print("PROBLEM")
            reward = 0
        return reward

    def best_child(self, node, factor):
        best_score = -10000000.0
        best_children = []
        for c in node.children:
            exploit = c.reward / c.visits
            explore = math.sqrt(math.log(2.0*node.visits)/float(c.visits))
            score = exploit + factor*explore
            if score == best_score:
                best_children.append(c)
            if score > best_score:
                best_children = [c]
                best_score = score
        # print(best_score)
        res = random.choice(best_children)
        # print(res.state._board)
        return res
