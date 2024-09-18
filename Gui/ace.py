import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个Matplotlib Figure和Canvas
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)

        # 绘制一个简单的图表
        self.ax.plot([1, 2, 3, 4, 5], [1, 4, 2, 5, 3])

        # 创建一个布局，并将Canvas添加到其中
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # 设置窗口标题和大小
        self.setWindowTitle('PyQt5 with Matplotlib')
        self.setGeometry(100, 100, 800, 600)

        # 显示窗口
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())