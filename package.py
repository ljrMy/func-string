import re,math
class FuncString:
    num_reg=re.compile(r'^[+\-]?\d+(\.\d+)?$')
    symbol=('+','-','*','/','%','^','\\','_','`',':',')')
    def __init__(self,code):
        self.code=code
        self.path=[]
        for expr in self.__resolve():
            method=expr[0]
            args=expr[1:]
            if method!=')' and not self.num_reg.match(args):
                raise Exception("Not a number.")
            if method!=')':
                args=float(args)
            if method=='+':
                self.path.append(lambda x,y=args:x+y)
            elif method=='-':
                self.path.append(lambda x,y=args:x-y)
            elif method=='*':
                self.path.append(lambda x,y=args:x*y)
            elif method=='/':
                self.path.append(lambda x,y=args:x/y)
            elif method=='%':
                self.path.append(lambda x,y=args:x%y)
            elif method=='^':
                self.path.append(lambda x,y=args:x**y)
            elif method=='\\':
                self.path.append(lambda x,y=args:x**(1/y))
            elif method=='_':
                self.path.append(lambda x,y=args:math.log(x,y))
            elif method==':':
                self.path.append(lambda x,y=args:round(x,int(y)))
            elif method==")":
                if args in dir(InnerFunction):
                    self.path.append(InnerFunction.__dict__[args])
                else:
                    raise Exception("Not a function.")
    def __resolve(self):
        result=""
        for i,j in enumerate(self.code):
            result+=j
            if i==len(self.code)-1:
                yield result
            elif self.code[i+1] in self.symbol and self.code[i] not in self.symbol:
                yield result
                result=''
    def __call__(self,x):
        for f in self.path:
            x=f(x)
        if x%1==0:
            return int(x)
        return x

class InnerFunction:
    def deg(x):
        return math.radians(x)
    def sin(x):
        return math.sin(x)
    def cos(x):
        return math.cos(x)
    def tan(x):
        return math.tan(x)
    def abs(x):
        return math.abs(x)
    def rec(x):
        return 1/x
    def term(x):
        if x%1!=0 or x<0:
            return -1
        elif x==0:
            return 0
        else:
            return InnerFunction.term(x-1)+x
    def fac(x):
        if x%1!=0 or x<0:
            return -1
        elif x==0:
            return 1
        else:
            return InnerFunction.term(x-1)*x
