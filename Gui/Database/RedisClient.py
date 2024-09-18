import redis

class RedisClient:
    def __init__(self,redis_server):
        self.redis = redis.Redis(**redis_server)
            
    def hmset(self,hash_key,fields):
        '''快速创建1个哈希字典''' 
        for key,val in fields.items():
            self.redis.hset(hash_key, key, val)
        
    def hgetall(self,hash_key):
        '''获取1个完整哈希字典'''
        return {field.decode('utf-8'):value.decode('utf-8') for field, value in self.redis.hgetall(hash_key).items()}
    
    def hmdel(self,hash_key):
        '''删除一个哈希字典'''
        self.redis.delete(hash_key)
     
    def keys_list(self):
        '''获取dedis内所有KEY'''
        return [byte.decode('utf-8') for byte in self.redis.keys('*') if not 'ticks' in byte.decode('utf-8')]
    
    def all_dict(self):
        key_all = self.keys_list()
        return [self.hgetall(key) for key in key_all]
    
    def zset_query(self,name,nmax):
        '''大于值查询'''
        return self.redis.zrangebyscore(name, nmax, float('inf'),withscores=True)
    