class Expr:
    def __add__(self, other): return Add(self, other)
    def __mul__(self, other): return Mul(self, other)
    def __pow__(self, other): return Power(self, other)

class Number(Expr):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return str(self.value)

class Variable(Expr):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class Add(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} + {self.right})"

class Mul(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} * {self.right})"

class Power(Expr):
    def __init__(self, base, exp):
        self.base = base
        self.exp = exp  
    def __repr__(self):
        return f"({self.base} ** {self.exp})"

class Sin(Expr):
    def __init__(self, arg):
        self.arg = arg
    def __repr__(self):
        return f"sin({self.arg})"

class Cos(Expr):
    def __init__(self, arg):
        self.arg = arg
    def __repr__(self):
        return f"cos({self.arg})"


def sym_diff(expr, var='x'):
    if isinstance(expr, Number):
        return Number(0)
    
    if isinstance(expr, Variable):
        return Number(1) if expr.name == var else Number(0)
    
    if isinstance(expr, Add):
        return Add(sym_diff(expr.left, var), sym_diff(expr.right, var))
    
    if isinstance(expr, Mul):
        f, g = expr.left, expr.right
        df = sym_diff(f, var)
        dg = sym_diff(g, var)
        return Add(Mul(df, g), Mul(f, dg))
    
    if isinstance(expr, Power):
        f, n = expr.base, expr.exp
        df = sym_diff(f, var)
        if isinstance(n, Number):
            new_exp = Number(n.value - 1)
            return Mul(Mul(n, Power(f, new_exp)), df)
        else:
            raise NotImplementedError("指數目前僅支援常數")
            
    if isinstance(expr, Sin):
        f = expr.arg
        df = sym_diff(f, var)
        return Mul(Cos(f), df)
        
    if isinstance(expr, Cos):
        f = expr.arg
        df = sym_diff(f, var)
        return Mul(Mul(Number(-1), Sin(f)), df)
        
    raise TypeError(f"未知的運算型態: {type(expr)}")
