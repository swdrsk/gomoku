class test1:
    def __init__(self):
        print 'test1_init'
    def print_s(self,s):
        print 'test1:'+s

if __name__=='__main__':
    t1 = test1()
    t1.print_s('hello world')
