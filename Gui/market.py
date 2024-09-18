import sys,time,json,datetime
from PyQt5.QtWidgets import QLineEdit,QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout,QHBoxLayout, QWidget,QSpacerItem,QSizePolicy,QPushButton,QMessageBox
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, QTimer
from .conn_data import connect_database
from .Database.base import market_base , signal_base

qt = {'name': 'Api_name', 'exchange': '交 易 所', 'apikey': 'Api_Key', 'secretkey': 'SecretKey', 'passphrase': 'PasspKey', 'type': '作    用', 'console': '运行状态','timestamp': '创建时间'}

class Market_Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.conn = connect_database()
        self.market_index = 0
        self.market_data = self.get_market()
        self.current_market = self.market_data[self.market_index]
        self.initUI()

        # Initialize timer for refreshing data every 10 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(10000)  # Refresh every 10 seconds (10000 milliseconds)


    def refresh_data(self):
        # Method to refresh market data and update UI
        self.market_data = self.get_market()
        self.current_market = self.market_data[self.market_index]
        self.initUI()

    def get_market(self):
        data = self.conn.select_redis()
        return data

    def initUI(self):
        self.setWindowTitle('行情情况')

        central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # 创建下拉框
        self.comboBox_layout()
        self.market_layout_widget()
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        # 创建一个 QWidget 作为主布局的容器
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)
        # self.show()

    def get_color(self):
        if int(time.time()*1000) < int(self.current_market.get('ective_timestamp')):
            color_text = """QComboBox {border: 1px solid #00cc99; /* 设置边框宽度、样式和颜色 */
                                           color: #00cc99;          /* 可选：设置内边距 */}
            QComboBox:popup {
                border: none; /* 如果需要，可以设置下拉菜单的边框样式 */
            }
        """
        else:
            color_text = """QComboBox {border: 1px solid #ff3366; /* 设置边框宽度、样式和颜色 */
                            color: #ff3366;}
            QComboBox:popup {
                border: none; /* 如果需要，可以设置下拉菜单的边框样式 */
            }
        """
        return color_text

    def comboBox_layout(self):
        self.comboBox_lable = QLabel('行情情况')
        self.comboBox = QComboBox()
        for index, item in enumerate(self.market_data):
            name = item.get('name')
            name = f'{name}      ✓' if int(time.time()*1000) < int(item.get('ective_timestamp')) else f'{name}      ✖'
            self.comboBox.addItem(name)
        
        color_text = self.get_color()
        
        self.comboBox.setStyleSheet(color_text)

        self.comboBox.setCurrentIndex(self.market_index)
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.main_layout.addWidget(self.comboBox_lable)
        self.main_layout.addWidget(self.comboBox)

    def on_combobox_changed(self, index):
        self.market_index = index
        self.current_market = self.market_data[self.market_index]
        self.initUI()

    def format_time(self,timestamp_ms):
        timestamp_s = int(timestamp_ms) / 1000
        dt_object = datetime.datetime.fromtimestamp(timestamp_s)
        date_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        return date_string

    def market_layout_widget(self):
        kline = json.loads(self.current_market.get('klines'))
        Label = QLabel(f"{self.current_market.get('name')}当前K线：")
        self.main_layout.addWidget(Label)
        for key,vlaue in kline.items():
            m_data = market_base(vlaue)
            Label = QLabel(f"{key}:{m_data.get_text()}")
            self.main_layout.addWidget(Label)

        exchange = self.current_market.get('exchange')
        Label = QLabel(f"交 易 所：{exchange}")
        self.main_layout.addWidget(Label)

        strategy = self.current_market.get('strategy')
        Label = QLabel(f"绑定策略：{strategy}")
        self.main_layout.addWidget(Label)

        symbol = self.current_market.get('symbol')
        Label = QLabel(f"交易对象：{symbol}")
        self.main_layout.addWidget(Label)

        gps= self.current_market.get('gps')
        Label = QLabel(f"坐    标：{gps}")
        self.main_layout.addWidget(Label)

        start_timestamp = self.format_time(self.current_market.get('start_timestamp'))
        Label = QLabel(f"创建时间：{start_timestamp}")
        self.main_layout.addWidget(Label)

        ective_timestamp = self.format_time(self.current_market.get('ective_timestamp'))
        Label = QLabel(f"更新时间：{ective_timestamp}")
        self.main_layout.addWidget(Label)

        state = json.loads(self.current_market['par'])
        state = state['data']['Now']['state']
        Label = QLabel(f"当前方向：{state}")
        self.main_layout.addWidget(Label)

        tradingSignal = json.loads(self.current_market['tradingSignal'])
        
        Label = QLabel("触发信号")
        self.main_layout.addWidget(Label)

        for item in tradingSignal:
            dest = signal_base(item)
            Label = QLabel(f"{dest.get_text()}")
            self.main_layout.addWidget(Label)
