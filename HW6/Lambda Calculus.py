import re

# ==========================================
# 1. 抽象語法樹 (AST) 節點定義
# ==========================================

class ASTNode:
    pass

class Var(ASTNode):
    """變數節點，例如: x"""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Abs(ASTNode):
    """λ 抽象節點，例如: \x. body 或 λx. body"""
    def __init__(self, param, body):
        self.param = param
        self.body = body

    def __repr__(self):
        return f"(λ{self.param}.{self.body})"

class App(ASTNode):
    """函數套用節點，例如: (M N)"""
    def __init__(self, fn, arg):
        self.fn = fn
        self.arg = arg

    def __repr__(self):
        return f"({self.fn} {self.arg})"


# ==========================================
# 2. 詞法與語法分析器 (Parser)
# ==========================================

def tokenize(text):
    """將輸入字串切分為 Token"""
    # 將 λ 統一轉換為 \
    text = text.replace('λ', '\\')
    token_specification = [
        ('LAMBDA', r'\\'),
        ('DOT',    r'\.'),
        ('LPAREN', r'\('), ('RPAREN', r'\)'),
        ('VAR',    r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('SKIP',   r'[ \t\n]+'),
    ]
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    tokens = []
    for mo in re.finditer(tok_regex, text):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        tokens.append((kind, value))
    return tokens

class Parser:
    def __init__(self, tokens, env=None):
        self.tokens = tokens
        self.pos = 0
        self.env = env or {}

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return (None, None)

    def consume(self, expected_kind=None):
        kind, val = self.peek()
        if expected_kind and kind != expected_kind:
            raise SyntaxError(f"預期 Token {expected_kind}，但得到 {kind} ({val})")
        self.pos += 1
        return val

    def parse(self):
        expr = self.parse_expression()
        if self.pos < len(self.tokens):
            raise SyntaxError(f"未解析完畢的語法，位於 Token: {self.peek()}")
        return expr

    def parse_expression(self):
        """解析表達式或套用 (Application)"""
        exprs = []
        while True:
            kind, val = self.peek()
            if kind in (None, 'RPAREN'):
                break
            exprs.append(self.parse_primary())

        if not exprs:
            raise SyntaxError("
