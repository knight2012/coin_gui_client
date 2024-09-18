from datetime import datetime, timezone

class market_base:
    def __init__(self,kw) -> None:
        self.t = self.format_time(kw[0])
        self.o = kw[1]
        self.h = kw[2]
        self.l = kw[3]
        self.c = kw[4]
        self.v = kw[5]
    
    def get_text(self):
        return f'{self.t}: 开盘价:{self.o} 最高价:{self.h} 最低价:{self.l} 收盘价:{self.c} 成交量:{self.v}'
    
    def format_time(self,timestamp_ms):
        timestamp_s = int(timestamp_ms) / 1000
        dt_object = datetime.fromtimestamp(timestamp_s)
        date_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        return date_string

class signal_base:
    def __init__(self,kw_text) -> None:
        self.x,self.p,self.f,self.r,self.l,self.t = kw_text.split('@')
        self.t = self.format_time(self.t)
    def get_text(self):
        return f'{self.x}-->价格:{self.p} 方向:{self.f} 风险:{self.r} 触发:{self.l} 触发时间:{self.t}'
    
    def format_time(self,timestamp_ms):
        timestamp_s = int(timestamp_ms) / 1000
        dt_object = datetime.fromtimestamp(timestamp_s)
        date_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        return date_string