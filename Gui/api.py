import sys,time
from PyQt5.QtWidgets import QLineEdit,QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout,QHBoxLayout, QWidget,QSpacerItem,QSizePolicy,QPushButton,QMessageBox
from .conn_data import connect_database
qt_data = {'name': 'Api_name', 'exchange': '交 易 所', 'apikey': 'Api_Key', 'secretkey': 'SecretKey', 'passphrase': 'PasspKey', 'type': '作    用', 'console': '运行状态','server':'主服务器','timestamp': '创建时间'}
qt_details = {"name": "标签名称：", "mode": "类型：(Z 以张成交，M 最小成交金额，TZ 张对冲 ,TM:资金对冲)", "unit": '价格单位：(1跳)', "amt": '资金金额：(最小额度)', "swap_qty": '期货数量：最小单位：', "spot_qty": '现货数量：最小单位', "mult": '倍数：'}                     

class Api_Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.conn = connect_database()
        self.account_api = self.update_apis()
        self.current_api = {}
        self.current_label = ''
        self.shared_apis = {}
        self.shared_details = {}
        self.initUI()

    def update_apis(self):
        data = self.conn.select_details()
        return data['data']

    def initUI(self):
        self.setWindowTitle('下拉数据和联动编辑')

        central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # 创建下拉框
        self.comboBox_layout()
        self.updata_data_widget()
        self.button_widget()
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        # 创建一个 QWidget 作为主布局的容器
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)
        # self.show()

    def comboBox_layout(self):
        
        self.comboBox_lable = QLabel('api:')
        self.comboBox = QComboBox()
        for key, item in self.account_api.items():
            self.comboBox.addItem(key)
            if not self.current_label in self.account_api:
                self.current_label = key
        
        if self.current_label in self.account_api:
            self.current_api = self.account_api.get(self.current_label)

        self.comboBox.setCurrentText(self.current_label)
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.main_layout.addWidget(self.comboBox_lable)
        self.main_layout.addWidget(self.comboBox)


    def button_widget(self):
        _qhb = QHBoxLayout()
        self.del_buttion = QPushButton('删除')
        self.modify_buttion = QPushButton('修改')
        self.add_buttion = QPushButton('添加')
        self.del_buttion.clicked.connect(self.del_event)
        self.modify_buttion.clicked.connect(self.modify_event)
        self.add_buttion.clicked.connect(self.add_event)
        _qhb.addWidget(self.del_buttion)
        _qhb.addWidget(self.modify_buttion)
        _qhb.addWidget(self.add_buttion)
        self.main_layout.addLayout(_qhb)

    def del_event(self):
        if self.current_api:
            account_id = self.current_api.get('id')
            reply = QMessageBox.question(self, 'Api 管 理', '你确定删除API吗？',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:

                self.conn.delete_details(account_id)
                self.account_api = self.update_apis()
                self.initUI()

    def modify_event(self):
        update_data = {key:item.text() for key,item in  self.shared_apis.items()}
        update_details  = {key:item.text() for key,item in  self.shared_details.items()}
        update_data.update({"details":update_details})

        reply = QMessageBox.question(self, '更 新 API', '你确定要更新数据吗？',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.conn.update_details(self.current_api.get('id'), update_data)
            self.current_api.update(update_data)


    def add_event(self):
        update_data = {key:item.text() for key,item in  self.shared_apis.items()}
        update_details  = {key:item.text() for key,item in  self.shared_details.items()}
        update_data.update({"details":update_details})
        reply = QMessageBox.question(self, '添 加 API 号', '你确定要加数据吗?',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.conn.insert_details(update_data)
            self.account_api = self.update_apis()
            self.initUI()
            

    def on_combobox_changed(self, index):
        self.current_label = self.comboBox.currentText()
        self.current_api = self.account_api[self.current_label]
        self.initUI()
        
    def updata_data_widget(self):

        self.data_widget = QHBoxLayout()
        self.data_left_widget = QVBoxLayout()
        self.data_right_widget = QVBoxLayout()

        for key,item in qt_data.items():
            _qhb = QHBoxLayout()
            Label = QLabel(qt_data.get(key))
            Label.setStyleSheet("QLabel { min-width: 55px; max-width: 55px; }")
            self.shared_apis[key] = QLineEdit(str(self.current_api.get(key)))
            _qhb.addWidget(Label)
            _qhb.addWidget(self.shared_apis[key])
            self.data_left_widget.addLayout(_qhb)

        details = self.current_api.get("details",{"name": "", "mode": "", "unit": "", "amt": "", "swap_qty": "", "spot_qty": "", "mult": ""}) 
        
        for key,item in details.items():
            Label = QLabel(qt_details.get(key))
            self.shared_details[key] = QLineEdit(str(item))
            self.data_right_widget.addWidget(Label)
            self.data_right_widget.addWidget(self.shared_details[key])

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.data_right_widget.addItem(spacer)
        
        self.data_widget.addLayout(self.data_left_widget)
        self.data_widget.addLayout(self.data_right_widget)
        self.main_layout.addLayout(self.data_widget)
