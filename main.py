import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from Gui.account import Account_Window
from Gui.api import Api_Window
from Gui.market import Market_Window
from Gui.tasks import Tasks_Window
from Gui.asset import Asset_Window

class TabExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('选项卡示例')
        self.setGeometry(100, 100, 600, 400)

        # 创建一个主布局，包含整体窗口的边距
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)  # 设置窗口的边距

        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        self.central_widget = QWidget()  # 创建一个中心部件来容纳主布局
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()
        tab5 = QWidget()

        tab_widget.addTab(tab1, '账号')
        tab_widget.addTab(tab2, 'Api管理')
        tab_widget.addTab(tab3, '行情')
        tab_widget.addTab(tab4, '任务')
        tab_widget.addTab(tab5, '资产曲线')

        # 在每个选项卡中添加一些内容
        self.add_tab_content_1(tab1)
        self.add_tab_content_2(tab2)
        self.add_tab_content_3(tab3)
        self.add_tab_content_4(tab4)
        self.add_tab_content_5(tab5)

    def add_tab_content_1(self, tab_widget):
        layout = QVBoxLayout()
        label = Account_Window()
        layout.addWidget(label)
        tab_widget.setLayout(layout)
    
    def add_tab_content_2(self, tab_widget):
        layout = QVBoxLayout()
        label = Api_Window()
        layout.addWidget(label)
        tab_widget.setLayout(layout)

    def add_tab_content_3(self, tab_widget):
        layout = QVBoxLayout()
        label = Market_Window()
        layout.addWidget(label)
        tab_widget.setLayout(layout)
    
    def add_tab_content_4(self, tab_widget):
        layout = QVBoxLayout()
        label = Tasks_Window()
        layout.addWidget(label)
        tab_widget.setLayout(layout)
    
    def add_tab_content_5(self, tab_widget):
        layout = QVBoxLayout()
        label = Asset_Window()
        layout.addWidget(label)
        tab_widget.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TabExample()
    window.show()
    sys.exit(app.exec_())
