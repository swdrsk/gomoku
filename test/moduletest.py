class test1:
    def __init__(self):
        self.point = 1
        self.value = 1
        print 'test1_init'
    def print_s(self,s):
        print 'test1:'+s
    def rewrite(self,point):
        print point, self.point
        value = point
        print value, self.value
        
if __name__=='__main__':
    t1 = test1()
    t1.print_s('hello world')
    t1.rewrite(19)
