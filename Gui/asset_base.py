import datetime
 

class asset_base():
    def __init__(self) -> None:
        pass
    
    def fomat_timestamp(self,timestamp_in_millis):
        timestamp_in_seconds = timestamp_in_millis / 1000
        dt_object = datetime.datetime.utcfromtimestamp(timestamp_in_seconds)
        return dt_object


    def update_asset(self,t,content):
        if not hasattr(self, 'timestamp'):
            setattr(self, 'timestamp', [self.fomat_timestamp(t)])
        else:
            value = getattr(self,'timestamp')
            value.append(self.fomat_timestamp(t))
            setattr(self, 'timestamp', value)
        
        for item in content:
            coin = item['coin']
            cashBal = item['cashBal']
            if not hasattr(self, coin):
                setattr(self, coin, [cashBal])
            else:
                value = getattr(self,coin)
                value.append(cashBal)
                setattr(self, coin, value)
        
        self.count = len(getattr(self,'timestamp'))
    
    def get_Data(self,coin):
        return getattr(self,'timestamp')[::-1] , getattr(self,coin)[::-1]