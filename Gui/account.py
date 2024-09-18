import sys
from PyQt5.QtWidgets import QLineEdit,QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout,QHBoxLayout, QWidget,QSpacerItem,QSizePolicy,QPushButton,QMessageBox
from .conn_data import connect_database
qt = {'user': '账  号:', 'password': '密  码:', 'name': '姓  名:', 'email': '邮  箱:', 'phone': '手  机:', 'grade': '权  限:', 'start_time': '时  间:'}

class Account_Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.conn = connect_database()
        self.current_index = 0
        self.account_data = self.update_account()
        if self.account_data:
            self.current_account = self.account_data[self.current_index]
        else:
            self.current_account = {}
        self.initUI()

    def update_account(self):
        data = self.conn.select_accounts()
        return data['data']['list']

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
        
        self.comboBox_lable = QLabel('账号：')
        self.comboBox = QComboBox()
        for index, item in enumerate(self.account_data):
            self.comboBox.addItem(item['user'])
        self.comboBox.setCurrentIndex(self.current_index)
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
        if self.current_account:
            account_id = self.current_account.get('id')
            reply = QMessageBox.question(self, '账 号 管 理', '你确定删除账号吗？',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:

                self.conn.delete_accounts(account_id)

                self.current_index = 0
                
                self.account_data = self.update_account()
                
                if self.account_data:

                    self.current_account = self.account_data[self.current_index]
                    
                else:
                    self.current_account = {}

                self.initUI()
                
                # self.updata_data_widget()

    def modify_event(self):
        update_data = {'user': self.user_Edit_.text(), 'password': self.password_Edit_.text(), 'name': self.name_Edit_.text(), 'email': self.email_Edit_.text(), 'phone': self.phone_Edit_.text(), 
                        'grade': self.grade_Edit_.text(),'start_time': self.grade_Edit_.text()}
        self.conn.update_account(self.current_account.get('id'),update_data)
        self.current_account.update(update_data)
        reply = QMessageBox.question(self, '更 新 账 号', '你确定要更新数据吗？',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.conn.update_account(self.current_account.get('id'), update_data)
            self.current_account.update(update_data)


    def add_event(self):
        update_data = {'user': self.user_Edit_.text(), 'password': self.password_Edit_.text(), 'name': self.name_Edit_.text(), 'email': self.email_Edit_.text(), 'phone': self.phone_Edit_.text(), 
                'grade': self.grade_Edit_.text()}
        reply = QMessageBox.question(self, '添 加 账 号', '你确定要加数据吗?',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.conn.insert_account(update_data)
            self.current_index = 0
            self.account_data = self.update_account()
            if self.account_data:
                self.current_account = self.account_data[self.current_index]
            else:
                self.current_account = {}

            self.initUI()
            


    def on_combobox_changed(self, index):
        self.current_index = index
        self.current_account = self.account_data[self.current_index]
        self.initUI()
    
    def updata_data_widget(self):
        # widgets_list = [self.data_widget.itemAt(i).widget() for i in range(self.data_widget.count()) if self.data_widget.itemAt(i) is not None]
        # try:
        #     if widgets_list:
        #         for widget in widgets_list:
        #             # 首先从布局中移除控件的项
        #             self.data_widget.removeItem(self.data_widget.itemAt(self.data_widget.indexOf(widget)))
        #             # 然后删除控件
        self.data_widget = QVBoxLayout()
        
        _qhb = QHBoxLayout()
        self.user_Label_ = QLabel(qt.get('user'))
        self.user_Label_.setStyleSheet("QLabel { min-width: 55px; max-width: 55px; }")
        self.user_Edit_ = QLineEdit(self.current_account.get('user'))
        _qhb.addWidget(self.user_Label_)
        _qhb.addWidget(self.user_Edit_)
        self.data_widget.addLayout(_qhb)

        _qhb = QHBoxLayout()
        self.password_Label_ = QLabel(qt.get('password'))
        self.password_Label_.setStyleSheet("QLabel { min-width: 55px; max-width: 55px; }")
        self.password_Edit_ = QLineEdit(self.current_account.get('password'))
        _qhb.addWidget(self.password_Label_)
        _qhb.addWidget(self.password_Edit_)
        self.data_widget.addLayout(_qhb)

        _qhb = QHBoxLayout()
        self.name_Label_ = QLabel(qt.get('name'))
        self.name_Label_.setStyleSheet("QLabel { min-width: 55px; max-width: 55px; }")
        self.name_Edit_ = QLineEdit(self.current_account.get('name'))
        _qhb.addWidget(self.name_Label_)
        _qhb.addWidget(self.name_Edit_)
        self.data_widget.addLayout(_qhb)

        _qhb = QHBoxLayout()
        self.email_Label_ = QLabel(qt.get('email'))
        self.email_Label_.setStyleSheet("QLabel { min-width: 55px; max-width: 55px; }")
        self.email_Edit_ = QLineEdit(self.current_account.get('email'))
        _qhb.addWidget(self.email_Label_)
        _qhb.addWidget(self.email_Edit_)
        self.data_widget.addLayout(_qhb)

        _qhb = QHBoxLayout()
        self.phone_Label_ = QLabel(qt.get('phone'))
        self.phone_Label_.setStyleSheet("QLabel { min-width: 55px; max-width: 55px; }")
        self.phone_Edit_ = QLineEdit(self.current_account.get('phone'))
        _qhb.addWidget(self.phone_Label_)
        _qhb.addWidget(self.phone_Edit_)
        self.data_widget.addLayout(_qhb)

        _qhb = QHBoxLayout()
        self.grade_Label_ = QLabel(qt.get('grade'))
        self.grade_Label_.setStyleSheet("QLabel { min-width: 55px; max-width: 55px; }")
        self.grade_Edit_ = QLineEdit(self.current_account.get('grade'))
        _qhb.addWidget(self.grade_Label_)
        _qhb.addWidget(self.grade_Edit_)
        self.data_widget.addLayout(_qhb)

        _qhb = QHBoxLayout()
        self.start_time_Label_ = QLabel(qt.get('start_time'))
        self.start_time_Label_.setStyleSheet("QLabel { min-width: 55px; max-width: 55px; }")
        self.start_time_Edit_ = QLineEdit(self.current_account.get('start_time'))
        _qhb.addWidget(self.start_time_Label_)
        _qhb.addWidget(self.start_time_Edit_)
        self.data_widget.addLayout(_qhb)

        self.main_layout.addLayout(self.data_widget)


    # except:
    #     import traceback
    #     traceback_info = traceback.format_exc()
    #     print(traceback_info)
    
    # def comboBox_add_Item(self):
    #     self.comboBox.clear()
    #     for index, item in enumerate(self.account_data):
    #         self.comboBox.addItem(item['user'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Account_Window()
    window.show()
    sys.exit(app.exec_())
