import sys
import matplotlib.dates as mdates
import datetime
from PyQt5.QtWidgets import QLineEdit,QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout,QHBoxLayout, QWidget,QSpacerItem,QSizePolicy,QPushButton,QMessageBox
from .conn_data import connect_database
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

qt = {'user': '账  号:', 'password': '密  码:', 'name': '姓  名:', 'email': '邮  箱:', 'phone': '手  机:', 'grade': '权  限:', 'start_time': '时  间:'}

class Asset_Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.conn = connect_database()
        self._cycle = 90
        self.asset_data = self.update_asset()
        self.current_label = ''
        self.current_coin = ''
        self.initUI()

    def update_asset(self):
        data = self.conn.select_assets(self._cycle)
        return data

    def initUI(self):
        self.setWindowTitle('下拉数据和联动编辑')

        central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # 创建下拉框
        self.comboBox_layout()
        self.canvas_widget()
        # self.button_widget()
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        # 创建一个 QWidget 作为主布局的容器
        self._info()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def _info(self):
        data = self.asset_data[self.current_label]
        timestamp,coin = data.get_Data(self.current_coin)
        min_ = min(coin)
        index = len(coin) - 1 - coin[::-1].index(min_)
        given_datetime = timestamp[index]
        current_datetime = datetime.datetime.now()
        difference = current_datetime - given_datetime
        days_difference = difference.days
        
        label_layout = QHBoxLayout()
        label_min = QLabel(f"{self.current_coin}曲线图,{self._cycle}天内最低数量：{min_}，当前数量：{coin[-1]},在{days_difference}天内收益率：{int(float(coin[-1])/float(min(coin))*100)-100}%")
        label_layout.addWidget(label_min)
        self.main_layout.addLayout(label_layout)

    def comboBox_layout(self):
        
        label_Layout = QHBoxLayout()
        self.account_comboBox_lable = QLabel('资金账户')
        self.coin_comboBox_lable = QLabel('币种')
        self.comboBox_cycle = QLabel('周期')
        label_Layout.addWidget(self.account_comboBox_lable)
        label_Layout.addWidget(self.coin_comboBox_lable)
        label_Layout.addWidget(self.comboBox_cycle)

        comboBox_Layout = QHBoxLayout()
        self.account_comboBox = QComboBox()
        for key, item in self.asset_data.items():
            self.account_comboBox.addItem(key)
            if not self.current_label in self.asset_data:
                self.current_label = key
        
        if self.current_label in self.asset_data:
            self.current_asset = self.asset_data.get(self.current_label).__dict__

        self.coin_comboBox = QComboBox()
        for key, item in self.current_asset.items():
            if key in ['timestamp','count']:
                continue
            self.coin_comboBox.addItem(key)
            current_asset = self.asset_data.get(self.current_label).__dict__
            if not self.current_coin in current_asset:
                self.current_coin = key

        self.cycle_comboBox = QComboBox()
        self.cycle_comboBox.addItems(['7','30','90','180','365','730','1095'])

        self.account_comboBox.setCurrentText(self.current_label)
        self.account_comboBox.currentIndexChanged.connect(self.on_account_comboBox_changed)
        self.coin_comboBox.setCurrentText(self.current_coin)
        self.coin_comboBox.currentIndexChanged.connect(self.on_coin_comboBox_changed)
        self.cycle_comboBox.setCurrentText(str(self._cycle))
        self.cycle_comboBox.currentIndexChanged.connect(self.on_cycle_comboBox_changed)

        comboBox_Layout.addWidget(self.account_comboBox)
        comboBox_Layout.addWidget(self.coin_comboBox)
        comboBox_Layout.addWidget(self.cycle_comboBox)

        self.main_layout.addLayout(label_Layout)
        self.main_layout.addLayout(comboBox_Layout)
    
    def canvas_widget(self):
        fig = Figure()
        ax = fig.add_subplot(111)
        self.canvas = FigureCanvas(fig)
        timestamp,data = self.asset_data[self.current_label].get_Data(self.current_coin)
        
        ax.plot(timestamp,data)

        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=10))

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))  # 每隔一天显示一个刻度
        fig.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.06)

        self.main_layout.addWidget(self.canvas)

    def on_account_comboBox_changed(self):
        self.current_label = self.account_comboBox.currentText()
        self.initUI()

    def on_coin_comboBox_changed(self):
        self.current_coin = self.coin_comboBox.currentText()
        self.initUI()

    def on_cycle_comboBox_changed(self):
        if self.cycle_comboBox.currentText() != str(self._cycle):
            self._cycle = self.cycle_comboBox.currentText()
            self.asset_data = self.update_asset()
        self.initUI()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Asset_Window()
    window.show()
    sys.exit(app.exec_())
