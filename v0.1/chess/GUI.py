import sys, time, os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

from chess import chessboard
from Algorithm import algorithm,evaluation
from Config.glo import *

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter 

# 定义线程类执行AI的算法
class AI(QtCore.QThread):
    
    finishSignal = QtCore.pyqtSignal(int, int)

    # 构造函数里增加形参
    def __init__(self, board, parent=None):
        super(AI, self).__init__(parent)
        self.board = board

    # 重写 run() 函数
    def run(self):
        self.ai = algorithm.Searcher()
        self.ai.board = self.board
        score, x, y = self.ai.search(2, 2)
        self.finishSignal.emit(x, y)

# 重新定义Label类
class LaBel(QLabel):

    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

class GoBang(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.chessboard = chessboard.ChessBoard()  # 棋盘类

        palette1 = QPalette()  # 设置棋盘背景
        palette1.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap('image/chessboard.jpg')))           # QPixmap 像素图控件
        self.setPalette(palette1)

        self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))           # 固定大小
        self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))

        self.setWindowTitle("GoBang")  # 窗口名称
        self.setWindowIcon(QIcon('image/black.png'))  # 窗口图标

        self.black = QPixmap('image/black.png')
        self.white = QPixmap('image/white.png')

        self.mouse_point = LaBel(self)  
        self.mouse_point.setPixmap(self.black)  # 加载黑棋
        self.mouse_point.setGeometry(270, 270, PIECE, PIECE)  #初始位置显示
        self.pieces = [LaBel(self) for i in range(255)]  # 新建棋子标签（棋盘最多容纳255个棋子）
        
        self.mouse_point.raise_()  # 鼠标始终在最上层
        self.ai_down = True  # 当值是False的时候说明AI正在思考，玩家鼠标点击失效

        self.setMouseTracking(True)
        self.show()

        self.piece_now = BLACK  # 黑棋先行
        self.step = 0  # 步数
        self.x, self.y = 1000, 1000

    def mouseMoveEvent(self, e):  # 黑色棋子随鼠标移动
        self.mouse_point.move(e.x() - 16, e.y() - 16)

    def coordinate_transform_map2pixel(self, i, j):
        # 从逻辑坐标到 UI 上的绘制坐标的转换
        return MARGIN + j * GRID - PIECE / 2, MARGIN + i * GRID - PIECE / 2

    def coordinate_transform_pixel2map(self, x, y):
        # 从 UI 上的绘制坐标到逻辑坐标的转换
        i, j = int(round((y - MARGIN) / GRID)), int(round((x - MARGIN) / GRID))        #四舍五入值
        # 越界
        if i < 0 or i >= N_board or j < 0 or j >= N_board:
            return None, None
        else:
            return i, j

    def drawLines(self, qp):  # 指示AI当前下的棋子
        if self.step != 0:
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(self.x - 5, self.y - 5, self.x + 3, self.y + 3)
            qp.drawLine(self.x + 3, self.y, self.x + 3, self.y + 3)
            qp.drawLine(self.x, self.y + 3, self.x + 3, self.y + 3)

    def paintEvent(self, event):  # 画出指示箭头
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def gameover(self, winner):
        if winner == BLACK:
            reply = QMessageBox.question(self, 'You Win!', 'Continue?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            reply = QMessageBox.question(self, 'You Lost!', 'Continue?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:  # 复位
            self.piece_now = BLACK
            self.mouse_point.setPixmap(self.black)
            self.step = 0
            for piece in self.pieces:
                piece.clear()
            self.chessboard.reset()
            self.update()
        else:
            self.close()

    def draw(self, i, j):
        x, y = self.coordinate_transform_map2pixel(i, j)

        if self.piece_now == BLACK:
            self.pieces[self.step].setPixmap(self.black)  # 放置黑色棋子
            self.piece_now = WHITE
            self.chessboard.put(i, j, BLACK)
        else:
            self.pieces[self.step].setPixmap(self.white)  # 放置白色棋子
            self.piece_now = BLACK
            self.chessboard.put(i, j, WHITE)

        self.pieces[self.step].setGeometry(x, y, PIECE, PIECE)  # 画出棋子
        self.step += 1  

        winner = self.chessboard.check()  # 判断输赢
        if winner != 0:
            self.mouse_point.clear()
            self.gameover(winner)

    def AI_draw(self, i, j):
        if self.step != 0:
            self.draw(i, j)  
            self.x, self.y = self.coordinate_transform_map2pixel(i, j)
        self.ai_down = True
        self.update()

    def mousePressEvent(self, e):  # 玩家下棋
        if e.button() == Qt.LeftButton and self.ai_down == True:
            x, y = e.x(), e.y()  # 鼠标坐标
            i, j = self.coordinate_transform_pixel2map(x, y)  
            if not i is None and not j is None:  
                if  self.chessboard.get_xy_on_logic_state(i,j) == 0:  # 棋子落在空白处
                    self.draw(i, j)
                    self.ai_down = False
                    board = self.chessboard.board()
                    self.AI = AI(board)  # 新建线程对象，传入棋盘参数
                    self.AI.finishSignal.connect(self.AI_draw)  # 结束线程，传出参数
                    self.AI.start()  # run

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GoBang()
    sys.exit(app.exec_())
