#! /usr/bin/env python  
# -*- coding: utf-8 -*-  
import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + '..\\')
import time  
from Algorithm_DFS import algorithm  
from Config.glo import *
from Seriall import serial_gob
from Seriall import serial_lan

#----------------------------------------------------------------------  
# chessboard: 棋盘类，简单从字符串加载棋局或者导出字符串，判断输赢等  
#----------------------------------------------------------------------  
class Chessboard (object):  
  
    def __init__ (self, forbidden = 0):  
        self.__board = [ [0 for n in range(N_board)] for m in range(N_board) ]  
        self.__forbidden = forbidden  
        self.__dirs = ( (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1) )  
        self.DIRS = self.__dirs  
        self.won = {}  
      
    # 清空棋盘  
    def reset (self):  
        for j in range(N_board):  
            for i in range(N_board):  
                self.__board[i][j] = 0  
        return 0  
      
    # 索引器  
    def __getitem__ (self, row):  
        return self.__board[row]  
  
    # 将棋盘转换成字符串  
    def __str__ (self):  
        # text = '  A B C D E F G H I J K L M N O\n' 
        text = ' ' 
        for i in range(N_board):
            text += ' ' + chr(65 + i)
        text += '\n'
        
        mark = ('. ', 'O ', 'X ')  
        nrow = 0  
        for row in self.__board:  
            line = ''.join([ mark[n] for n in row ])  
            text += chr(ord('A') + nrow) + ' ' + line  
            nrow += 1  
            if nrow < N_board: text += '\n'  
        return text  
      
    # 转成字符串  
    def __repr__ (self):  
        return self.__str__()  
  
    def get (self, row, col):  
        if row < 0 or row >= N_board or col < 0 or col >= N_board:  
            return 0  
        return self.__board[row][col]  
  
    def put (self, row, col, x):  
        if row >= 0 and row < N_board and col >= 0 and col < N_board:  
            self.__board[row][col] = x  
        return 0  
      
    # 判断输赢，返回0（无输赢），1（白棋赢），2（黑棋赢）  
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
      
    # 返回数组对象  
    def board (self):  
        return self.__board  
      
    # 导出棋局到字符串  
    def dumps (self):  
        import io
        sio = io.StringIO()  
        board = self.__board  
        for i in range(N_board):  
            for j in range(N_board):  
                stone = board[i][j]  
                if stone != 0:  
                    ti = chr(ord('A') + i)  
                    tj = chr(ord('A') + j)  
                    sio.write('%d:%s%s '%(stone, ti, tj))  
        return sio.getvalue()  
      
    # 从字符串加载棋局  
    def loads (self, text):  
        self.reset()  
        board = self.__board  
        for item in text.strip('\r\n\t ').replace(',', ' ').split(' '):  
            n = item.strip('\r\n\t ')  
            if not n: continue  
            n = n.split(':')  
            stone = int(n[0])  
            i = ord(n[1][0].upper()) - ord('A')  
            j = ord(n[1][1].upper()) - ord('A')  
            board[i][j] = stone  
        return 0  
  
    # 设置终端颜色  
    def console (self, color):  
        if sys.platform[:3] == 'win':  
            try: import ctypes  
            except: return 0  
            kernel32 = ctypes.windll.LoadLibrary('kernel32.dll')  
            GetStdHandle = kernel32.GetStdHandle  
            SetConsoleTextAttribute = kernel32.SetConsoleTextAttribute  
            GetStdHandle.argtypes = [ ctypes.c_uint32 ]  
            GetStdHandle.restype = ctypes.c_size_t  
            SetConsoleTextAttribute.argtypes = [ ctypes.c_size_t, ctypes.c_uint16 ]  
            SetConsoleTextAttribute.restype = ctypes.c_long  
            handle = GetStdHandle(0xfffffff5)  
            if color < 0: color = 7  
            result = 0  
            if (color & 1): result |= 4  
            if (color & 2): result |= 2  
            if (color & 4): result |= 1  
            if (color & 8): result |= 8  
            if (color & 16): result |= 64  
            if (color & 32): result |= 32  
            if (color & 64): result |= 16  
            if (color & 128): result |= 128  
            SetConsoleTextAttribute(handle, result)  
        else:  
            if color >= 0:  
                foreground = color & 7  
                background = (color >> 4) & 7  
                bold = color & 8  
                sys.stdout.write(" \033[%s3%d;4%dm"%(bold and "01;" or "", foreground, background))  
                sys.stdout.flush()  
            else:  
                sys.stdout.write(" \033[0m")  
                sys.stdout.flush()  
        return 0  
      
    # 棋局输出  
    def show (self):  
        # print('  A B C D E F G H I J K L M N O')  
        text = ' ' 
        for i in range(N_board):
            text += ' ' + chr(i+65)
        text == '\n'
        print(text)
        mark = ('. ', 'O ', 'X ')  
        nrow = 0  
        self.check()  
        color1 = 10  
        color2 = 13  
        for row in range(N_board):  
            print( chr(ord('A') + row), end=' '),  
            for col in range(N_board):  
                ch = self.__board[row][col]  
                if ch == 0:   
                    self.console(-1)  
                    print('.', end=' '),  
                elif ch == 1:  
                    if (row, col) in self.won:  
                        self.console(9)  
                    else:  
                        self.console(10)  
                    print ('O', end=' '),  
                    #self.console(-1)  
                elif ch == 2:  
                    if (row, col) in self.won:  
                        self.console(9)  
                    else:  
                        self.console(13)  
                    print ('X', end=' '),  
                    #self.console(-1)  
            self.console(-1)  
            print('')  
        return 0  
  
from Algorithm_DFS import algorithm
import get_chessboard_info

#----------------------------------------------------------------------  
# main game  
#----------------------------------------------------------------------  
class GobangAI( Chessboard):

    def __init__ (self):
        Chessboard.__init__(self)
        self.turn = 1
        self.history = []
        self.undo = False      # 悔棋 
        self.DEPTH = 1         # 设置难度   1 2

        self.s = algorithm.Searcher()  
        self.s.board = self.board()  

        self.ser_gobang = serial_gob.marlin_serial()
        self.ser_gobang.start()
        self.ser_gobang.get_ready()


    def get_action(self):
        pass
    
    def main(self):
        queue_history = []
        
        # ser_lan = serial_lan.speak_serial()
        # ser_lan.start()
        
        while 1:  
            print ('')  
            # 获得用户动作：下子/悔棋/退出
            while_time = 0
            while 1:  
                # # 检测语音
                # while_time += 1
                # if while_time == 1:
                #     tmp = ser_lan.get_info()
                #     if tmp == None:
                #         while_time = 0
                #     else:
                #         if tmp[-1] == 1:
                #             print('01')
                #             self.undo = True  
                #             break 
                #         elif tmp[-1] == 2:
                #             print('02')
                #             print (self.dumps())  
                #             return 0 
                
                print ('<ROUND %d>'%(len(self.history) + 1))  
                self.show()  
                print ('Your move (u:undo, q:quit):'),  
                # text = input('please move').strip('\r\n\t ') 
                print(self.turn)
                queque = get_chessboard_info.get_chessboard_green(self.turn)
                x, y = 100, 100
                for i in queque[-1:]:               
                    if i not in queue_history:
                        queue_history.append(i)
                        (x, y) = i
                        print('break')                
                        break
                text = chr(65 + y) + chr(65 + x)
                print(text)
                if len(text) == 2:  
                    tr = ord(text[0].upper()) - ord('A')  
                    tc = ord(text[1].upper()) - ord('A')  
                    if tr >= 0 and tc >= 0 and tr < N_board and tc < N_board:  
                        if self[tr][tc] == 0:  
                            row, col = tr, tc  
                            break  
                        else:  
                            print ('can not move there')  
                    else:  
                        print ('bad position')  
                elif text.upper() == 'U':  
                    self.undo = True  
                    break  
                elif text.upper() == 'Q':  
                    print (self.dumps())  
                    return 0  
            
            # 悔棋 
            if self.undo == True:  
                self.undo = False  
                if len(self.history) == 0:  
                    print ('no history to undo')  
                else:  
                    print ('rollback from history ...')  
                    move = self.history.pop()  
                    self.loads(move)
                    
                    # print('queue_his:', queue_history[-1])

                    get_chessboard_info.chessboard_info_green = get_chessboard_info.chessboard_info_green[:-1]
                    self.turn -= 1

                    # y, x = queue_history[-1]
                    # row, col = y, x
                    print("row. col:", row, col)
                    t_x, t_y = row*2+2, col*2+2
                    #TODO:@libing
                    self.ser_gobang.send_undo_info(100*t_x, 100*t_y+50, 20000)

            # 下子
            else:  
                self.turn += 1
                self.history.append(self.dumps())  
                self[row][col] = 1  
    
                if self.check() == 1:  
                    self.show()  
                    print (self.dumps())  
                    print ('')  
                    print ('YOU WIN !!')  
                    return 0  
    
                print ('robot is thinking now ...')  
                # 算法决策！！！
                if self.turn == 2:
                    score, row, col = 0,  row+1, col+1
                else:
                    score, row, col = self.s.search(2, self.DEPTH)  
                cord = '%s%s'%(chr(ord('A') + row), chr(ord('A') + col))  
                print ('robot move to %s (%d)'%(cord, score))  
                
                print("row. col:", row, col)
                self.ser_gobang.pick_up()
                time.sleep(2)
                t_row, t_col = row, col
                self.ser_gobang.pick_down(t_row, t_col)

                self[row][col] = 2  
    
                if self.check() == 2:  
                    self.show()  
                    print (self.dumps())  
                    print ('')  
                    print ('YOU LOSE.')  
                    return 0  
  
        return 0  
  
  
#----------------------------------------------------------------------  
# testing case  
#----------------------------------------------------------------------  
if __name__ == '__main__':  

    temp_a = GobangAI()
    temp_a.main()