from Config.glo import *

# 定义棋盘类
class ChessBoard(object):

    def __init__(self):
        self.__board = [[0 for n in range(N_board)] for m in range(N_board)]

    # 清空棋盘  
    def reset (self):  
        for j in range(N_board):  
            for i in range(N_board):  
                self.__board[i][j] = 0  
        return 0

    # 返回数组对象
    def board(self):  
        return self.__board

    def get (self, row, col):  
        if row < 0 or row >= N_board or col < 0 or col >= N_board:  
            return 0  
        return self.__board[row][col]  

    def put(self, row, col, x):  
        if row >= 0 and row < N_board and col >= 0 and col < N_board:  
            self.__board[row][col] = x  
        return 0  

    # 获取指定点坐标的状态
    def get_xy_on_logic_state(self, x, y):  
        return self.__board[x][y]

    # 获取指定点的指定方向的状态
    def get_xy_on_direction_state(self, point, direction):  
        if point is not False:
            x = point[0] + direction[0]
            y = point[1] + direction[1]
            if x < 0 or x >= N_board or y < 0 or y >= N_board:
                return False
            else:
                return self.__board[x][y]

    # 判断输赢  
    def check (self):  
        board = self.__board  
        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))  
        for i in range(N_board):  
            for j in range(N_board):  
                if board[i][j] == 0: continue  
                id = board[i][j]  
                for d in dirs:  
                    x, y = j, i  
                    count = 0  
                    for k in range(5):  
                        if self.get(y, x) != id: break  
                        y += d[0]  
                        x += d[1]  
                        count += 1  
                    if count == 5:  
                        self.won = {}  
                        r, c = i, j  
                        for z in range(5):  
                            self.won[(r, c)] = 1  
                            r += d[0]  
                            c += d[1]  
                        return id  
        return 0  
