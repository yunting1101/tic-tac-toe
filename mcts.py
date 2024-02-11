import math
import random

class tree_node():#建立mcts的節點
    def __init__(self, board, parent):
        self.board = board
        if self.board.game_win() or self.board.game_draw():
            self.is_terminal = True
        else:
            self.is_terminal = False
        
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        self.visits = 0
        self.score = 0
        self.children = {}

class MCTS():
    def search(self, initial_state):#搜尋下一步移動位置
        self.root = tree_node(initial_state, None)
        for iteration in range(1000):#選擇一個node
            node = self.select(self.root)
            score = self.rollout(node.board)
            self.backpropagate(node, score)

        try:
            return self.get_best_move(self.root, 0)
        except:
            pass

    def select(self, node):
        while not node.is_terminal:#確認處理的不是終節點
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
            else:
                return self.expand(node)
            
        return node
    
    def expand(self, node):#找該節點合理的下一個移動位置
        states = node.board.generate_states()
        for state in states:
            if str(state.position) not in node.children:#新增child node
                new_node = tree_node(state, node)
                node.children[str(state.position)] = new_node

                if len(states) == len(node.children):
                    node.is_fully_expanded = True

                return new_node
            
        print('should not expand')

    def rollout(self, board):#隨機移動
        while not board.game_win():
            try:
                board = random.choice(board.generate_states())
            except:
                return 0

        if board.player2 == 'x':
            return 1
        elif board.player2 == 'o':
            return -1

    def backpropagate(self, node, score):#反向傳播visit和score
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent

    def get_best_move(self, node, exploration_constant):#選擇下一步的最佳解
        best_score = float('-inf')
        best_moves = []

        for child_node in node.children.values():
            if child_node.board.player2 == 'x':
                current_player = 1
            elif child_node.board.player2 == 'o':
                current_player = -1

            move_score = current_player * child_node.score / child_node.visits + exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))
            #print('move_score:', move_score)
            if move_score > best_score:#若新的score大於原本的則更新
                best_score = move_score
                best_moves = [child_node]
            elif move_score == best_score:
                best_moves.append(child_node)

        return random.choice(best_moves)
