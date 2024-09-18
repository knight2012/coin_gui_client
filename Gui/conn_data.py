from .Database.fmysql import conect_mysql
from .Database.RedisClient import RedisClient
from .asset_base import asset_base
import connt as connt,datetime
import time
import json

class connect_database(object):
    def __init__(self):
        self.conn = conect_mysql(connt.server)
        self.redis = RedisClient(connt.redis_server)
    
    def get_timestamp(self,days = False):
        now = datetime.datetime.now()
        re_peplace = {'minute':0,'second':0,'microsecond':0}
        if days:
            re_peplace['hour'] = 0
        timestamp = int(now.replace(**re_peplace).timestamp())
        return timestamp*1000
    
    def revert_timestamp(self,revert):
        t_date = datetime.datetime.now() - datetime.timedelta(days=revert)
        re_peplace = {'hour':23,'minute':59,'second':59,'microsecond':0}
        timestamp = int(t_date.replace(**re_peplace).timestamp())
        return timestamp*1000

    def insert_account(self,data):
        self.conn.insert('account',[*[val for val in data.values()],int(time.time())])
        return {'code':'200','msg':'Created success'}

    def select_account(self,user):
        result = self.conn.select('account', user = user)
        return result
    
    def update_account(self,id,data:dict,user : str = ''):
        if user :
            self.conn.update('account', data , id = id, user = user)
        else:
            self.conn.update('account',data,id = id)
        rest = self.conn.select('account',id = id)
        rest = {'id':rest[-1]['id'],'account':rest[-1]['user'],'name':rest[-1]['name'],'tel':rest[-1]['phone'],'email':rest[-1]['email']}
        return {'code':'200','data':rest,'msg':'updata success'}
    
    def select_accounts(self,start = 0,mun = 10000000):
        result = self.conn.select('account',0,10000000)
        result = result[::-1]
        return {'code':'200','data':{'list':result[start:start+mun],'total':len(result)},'msg':'updata success'}
    
    def delete_accounts(self,account_id:int):
        self.conn.re_del('account',account_id)
        return {'code':'200','data':{},'msg':'delete success'}
    
    def format_assets(self,asset_data):
        data =[json.loads(item['data']) for item in asset_data]
        base = asset_base()
        for item in data:
            base.update_asset(item['timestamp'],item['content'])
        return base

    def select_assets(self,days = 30):
        revert_day = self.revert_timestamp(days)
        sztimestamp = "{}_{}".format('>=',revert_day)
        re = self.conn.select("assets" ,0,10000000, timestamp = sztimestamp)
        result={}
        for item in re:
            name = item['status']
            if name not in result:
                result[name] = {}
                s = list(filter(lambda x:x['status'] == name ,re))
                result[name] = self.format_assets(s)
        return result
    

    def insert_details(self,data):
        name = data.get('name')
        account_name,account_label = name.split('_')
        updata = json.dumps(data)
        data = {'timestamp':int(time.time()*1000),'name':data.get('name'),'data':updata,'type':data.get('type'),'console':data.get('console'),'server':data.get('server'),'status':account_name}
        self.conn.insert('apis',[*[val for val in data.values()]])
        return {'code':'200','data':{},'msg':'create details success'}

    def select_details(self,start = 0,mun = 100000):
        result = self.conn.select("apis" ,start,mun)
        result = {item['name']:{'id':item['id'],'types': item['types'], 'console': item['console'], 'server': item['server'],**json.loads(item['data'])} for item in result}
        return {'code':'200','data':result,'msg':''}
    
    def update_details(self,id,data:dict,user = ''):
        try:
            updata = {'name': data.get('name'),'data':json.dumps(data),'types':data.get('type'),'console':data.get('console'),'server': data.get('server')}
            self.conn.update('apis', updata , id = id)
        except Exception as e:
            import traceback
            traceback_info = traceback.format_exc()
            print(traceback_info)
        return {'code':'200','data':{},'msg':'updata success'}
    
    
    def delete_details(self,account_id:int):
        self.conn.re_del('apis',account_id)
        return {'code':'200','data':{},'msg':'delete success'}
    
    def insert_marketdata(self,data):
        try:
            self.conn.insert('marketdata',[*[val for val in data.values()]])
            return {'code':'200','data':{},'msg':'create details success'}
        except Exception as e:
            err = e.args[0]
            if err['code'] == 1062:
                return {'code':'1062','data':{},'msg':f"{err['msg']}重名了"}
        
    def select_marketdata(self,start = 0,mun = 10000000):
        result = self.conn.select("marketdata" ,start,mun)
        
        result = [{'id':item['id'],**json.loads(item['data'])} for item in result]
        return {'code':'200','data':{'list':result[start:start+mun],'total':len(result),'strategy':self.select_strategy()},'msg':'updata success'}
    
    def delete_marketdata(self,account_id:int):
        self.conn.re_del('marketdata',account_id)
        return {'code':'200','data':{},'msg':'delete success'}
    
    def select_orders(self, start = 0, mun = 10):
        result = self.conn.select("orders",start = start, mun = mun)
        return result
    
    def insert_order(self,data):
        self.conn.insert('orders',[*[val for val in data.values()]])
        return {'code':'200','data':{},'msg':'create order success'}
    
    def select_strategy(self,start = 0,mun = 10000000):
        result = self.conn.select("strategy" ,start,mun)
        result = {item['strategy']:item for item in result}
        return result
    
    def select_error(self,user,start=0,mun =10):
        result = self.conn.select("error",start = start, mun = mun,status = user)
        return result
    
    def select_qlink(self,user,start=0,mun =10):
        result = self.conn.select("qlink",start = start, mun = mun,status = user)
        return result
    
    def select_Fuzzy(self,user):
        
        def _re(item):
            rest = json.loads(item)
            rest['ective_timestamp'] = int(time.time())
            return rest
                        
        result = self.conn.select_Fuzzy("orders",'status',user)
        result = [_re(item['data']) for item in result]
        return result
    
    def updata_task(self,id):
        updata = {'manual':1}
        self.conn.update('orders', updata , id = id)
        return{'code':'200','data':{},'msg':'updata order success'}
    
    def select_redis(self):
        result = self.redis.all_dict()
        return result
    
    
if __name__ == '__main__':
    a = connect_database()
    z = a.select_Fuzzy('ch2012')
    print(z)
    # e = {}
    # for item in z:
    #     if item.get('strategy') in e:
    #         e[item.get('strategy')].append(item)
    #     else:
    #         e[item.get('strategy')] = [item]
    # print(e)
