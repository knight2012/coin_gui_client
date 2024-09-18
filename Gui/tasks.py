import sys,time,json,datetime
from PyQt5.QtWidgets import QLineEdit,QApplication, QMainWindow, QTreeView,QLabel, QComboBox, QVBoxLayout,QHBoxLayout, QWidget,QSpacerItem,QSizePolicy,QPushButton,QMessageBox
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QTimer
from .conn_data import connect_database
from .Database.base import market_base , signal_base
qt = {'id': '编号：', 't': '下单时间：', 'ex': '交 易 所：', 'sty': '策略：', 'sy': '交易品：','i': '执行中：', 'bias':'偏移值：','z': '主仓：', 'long': '多头持仓：', 'short': '空头持仓：', 'market': '触发信号：', 
        'shape': '形态：', 'gps': '定位坐标：','bmast': '计划主仓：','bslar': '计划对冲：','pmast': '计划平主仓：', 'pslar': '计划平对冲：', 'Mobile_re': '移动平仓：','warning': '警告：', 'discard':'状态：'}

class Tasks_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conn = connect_database()
        self.current_task = {}
        self.current_id = ''
        self.tasks_info = {}
        self.tasks_data = self.get_tasks()
        self.initUI()

        # Initialize timer for refreshing data every 10 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(10000)

    def refresh_data(self):
        # Method to refresh market data and update UI
        tasks_data = self.get_tasks()
        if self.tasks_data.keys() != tasks_data.keys():
            self.update_tree()
        else:
            self.tasks_right()

    def add_ma(self,pn1,pn2):
        p1,n1 = pn1
        p2,n2 = pn2
        if n2 == 0:
            return [p1,n1]
        elif p1 != 0: 
            mun = float(n1)+float(n2)
            p = mun/(float(n1)/float(p1)+float(n2)/float(p2))
            return [p,mun]
        else:
            return [p2,n2]
        
    def get_tasks(self):
        tasks_data = {}
        data = self.conn.select_orders()
        biao = {'tasks':len(data),'run':0,'stop':0,'long':[0,0],'short':[0,0]}
        for item in data:
            label = item.get('status')
            if label not in tasks_data:
                filter_data = list(filter(lambda x: x['status'] == label, data))
                tasks_data[label] = list(sorted(filter_data, key=lambda x: int(x['id'])))
            if not self.current_id:
                self.current_id = item.get('id')
            sw_data = json.loads(item.get('data'))
            if item.get('discard') == 0:
                biao['long'] = self.add_ma(biao['long'],sw_data['long'])
                biao['short'] = self.add_ma(biao['short'],sw_data['short'])
                biao['run'] += 1
        biao['stop'] = biao['tasks'] - biao['run']
        self.tasks_info = biao
        if hasattr(self, 'data_info_widget'):
            self.Refresh_info()
        return tasks_data

    def initUI(self):
        self.setWindowTitle('任务情况')

        central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # 创建下拉框
        self.tasks_layout_widget()
        # spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.main_layout.addItem(spacer)
        # 创建一个 QWidget 作为主布局的容器
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)
        # self.show()

    def format_time(self, timestamp_ms,standard=False):
        timestamp_s = int(timestamp_ms)
        dt_object = datetime.datetime.fromtimestamp(timestamp_s)
        text_label = '%Y-%m-%d %H:%M:%S' if standard else '%Y%m%d %H:%M:%S'
        date_string = dt_object.strftime(text_label)
        return date_string if standard else date_string[2:] 

    def tasks_layout_widget(self):
        self.data_widget = QHBoxLayout()
        self.data_left_widget = QVBoxLayout()
        self.data_right_widget = QVBoxLayout()
        self.tasks_left()
        self.tasks_right()
        self.data_info_widget = QVBoxLayout()
        self.Refresh_info()
        self.data_widget.addLayout(self.data_left_widget)
        self.data_widget.addLayout(self.data_right_widget, 3)
        self.main_layout.addLayout(self.data_widget)
        self.main_layout.addLayout(self.data_info_widget)

    def Refresh_info(self):
        info = f"任务数量：{self.tasks_info.get('tasks')}  运行中：{self.tasks_info.get('run')}  停止中：{self.tasks_info.get('stop')}  多头总持仓：{self.tasks_info.get('long')} 空头总持仓：{self.tasks_info.get('short')}"
        if hasattr(self, 'data_info'):
            self.data_info.setText(info)
        else:
            self.data_info = QLabel(info)
            self.data_info_widget.addWidget(self.data_info)
        
    def tasks_left(self):
        self.tree = QTreeView()
        self.tree.setFixedWidth(210)
        self.tree.setHeaderHidden(True)

        self.model = QStandardItemModel()
        self.root_node = self.model.invisibleRootItem()

        for key, dictvalue in self.tasks_data.items():
            tree_item = QStandardItem(key)
            self.root_node.appendRow(tree_item)
        
            for item in dictvalue:
                error_info = 'stop' if int(item.get('discard')) != 0 else 'Run'
                name = f"{item.get('id')}_{error_info}_{self.format_time(item.get('timestamp'))}"
                subitem = QStandardItem(name)
                tree_item.appendRow(subitem)
        self.tree.setModel(self.model)
        self.tree.setEditTriggers(QTreeView.NoEditTriggers)
        self.tree.clicked.connect(self.on_tree_view_clicked)
        self.data_left_widget.addWidget(self.tree)

    def tasks_right(self):

        while self.data_right_widget.count():
            child = self.data_right_widget.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for key,value in qt.items():
            if key == 'z':
                label = '多头' if self.current_task.get(key) == '1' else '空头'
                lable = QLabel(f"{value}{label}")
                self.data_right_widget.addWidget(lable)
                continue
            elif key == 't':
                text_time = self.format_time(self.current_task.get(key),True) if self.current_task.get(key) else None
                lable = QLabel(f"{value}{text_time}")
                self.data_right_widget.addWidget(lable)
                continue
            lable = QLabel(f"{value}{self.current_task.get(key)}")
            self.data_right_widget.addWidget(lable)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.data_right_widget.addItem(spacer)

    def update_tree(self):
        self.model.clear()
        self.root_node = self.model.invisibleRootItem()
        for key, dictvalue in self.tasks_data.items():
            tree_item = QStandardItem(key)
            self.root_node.appendRow(tree_item)
            for item in dictvalue:
                error_info = 'stop' if int(item.get('discard')) != 0 else 'Run'
                name = f"{item.get('id')}_{error_info}_{self.format_time(item.get('timestamp'))}"
                subitem = QStandardItem(name)
                tree_item.appendRow(subitem)
        self.tree.setModel(self.model)
        self.tree.expandAll()
    
    def on_tree_view_clicked(self, index):
        
        item = self.model.itemFromIndex(index)
        parent_item = item.parent()
        if parent_item:
            text_s = item.text()
            self.current_id = text_s.split('_')[0]
            current_data = self.tasks_data.get(parent_item.text())
            current_data = list(filter(lambda x:str(x['id']) == str(self.current_id),current_data))
            self.current_task = json.loads(current_data[-1]['data'])
        self.tasks_right()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Tasks_Window()
    window.show()
    sys.exit(app.exec_())
