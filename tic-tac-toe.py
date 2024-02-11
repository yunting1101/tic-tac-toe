from copy import deepcopy
from mcts import *

class Board():
    def __init__(self, board = None):
        self.player1 = 'x'#當前由誰下棋(還未下)
        self.player2 = 'o'
        self.empty = '.'

        self.position = {}
        self.init_board()

        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)
    
    def init_board(self):# 初始九宮格
        for row in range(3):
            for col in range(3):
                self.position[row, col] = self.empty

    def make_move(self, row, col):# 交換下棋者
        board = Board(self)
        board.position[row, col] = self.player1 

        (board.player1, board.player2) = (board.player2, board.player1)

        return board

    def game_draw(self):#所有格子填滿，遊戲結束
        for row, col in self.position:
            if self.position[row, col] == self.empty:
                return False
        return True
    
    def game_win(self):#連成直線獲勝
        #直向
        for col in range(3):
            winning_sequence = []
            for row in range(3):
                if self.position[row, col] == self.player2:
                    winning_sequence.append((row, col))
                if len(winning_sequence) == 3:
                    return True
        #橫向
        for row in range(3):
            winning_sequence = []
            for col in range(3):
                if self.position[row, col] == self.player2:
                    winning_sequence.append((row, col))
                if len(winning_sequence) == 3:
                    return True
        #斜線
        winning_sequence = []

        for row in range(3):
            col = 3 - row - 1
            if self.position[row, col] == self.player2:
                winning_sequence.append((row, col))
            if len(winning_sequence) == 3:
                return True
            
        winning_sequence = []

        for row in range(3):
            col = row
            if self.position[row, col] == self.player2:
                winning_sequence.append((row, col))
            if len(winning_sequence) == 3:
                return True
        #無人贏
        return False
    
    def generate_states(self):#產生在目前位置進行的可行走法
        actions = []
        for row in range (3):
            for col in range (3):
                if self.position[row, col] == self.empty:#若該格子為空，則可走
                    actions.append(self.make_move(row, col))

        return actions
    
    def game_loop(self):
        print('\nTic-Tac-Toe\n')
        print('enter "exit" to quit this game')
        print('enter move like: 1,2 for x axis and y axis')
        print('(1,1) (2,1) (3,1)\n(1,2) (2,2) (3,2)\n(1,3) (2,3) (3,3)')

        print(self)
        Mcts = MCTS()
        
        while True:
            user_input = input('enter move or exit:')#玩家輸入
            if user_input == 'exit':
                break
            if user_input == '':
                continue
            try:
                row = int(user_input.split(',')[1]) - 1
                col = int(user_input.split(',')[0]) - 1

                if self.position[row, col] != self.empty:#判斷該位置是否已有標記
                    print('Illegal move')
                    continue

                self = self.make_move(row, col)
                print(self)
                #AI移動......
                best_move = Mcts.search(self)
                try:
                    self = best_move.board
                except:
                    pass

                print(self)

                if self.game_win():#若有人贏了
                    print('player "%s" has won the game!\n' % self.player2)
                    break
                elif self.game_draw():#無人贏但格子填滿
                    print('Game is drawn!\n')
                    break
            except Exception as excpt:#輸入錯誤格式或內容
                print('Error:', excpt)
                print('Illegal command......QAQ')
                print('enter move like: 1,2 for x axis and y axis')

    def __str__(self):# 輸出九宮格及目前由誰下棋
        board_string = ''
        for row in range(3):# 3*3輸出九宮格
            for col in range(3):
                board_string+=' %s' % self.position[row, col]
            board_string+='\n'
        if self.player1 == 'x':
            board_string = '\n------------\n"x" to move:\n------------\n\n' + board_string
        elif self.player1 == 'o':
            board_string = '\n------------\n"o" to move:\n------------\n\n' + board_string
        return board_string

# main
if __name__ == '__main__':
    board = Board()
    
    board.game_loop()
