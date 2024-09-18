class conn(object):
    def __init__(self,**kwargs):
        self.host = kwargs.get('host')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.database = kwargs.get('database')
        self.prefix = kwargs.get('prefix')
        
if __name__ == '__main__':
    a ="adfadfa"
    a = (a,)
    
    print(a,type(a))