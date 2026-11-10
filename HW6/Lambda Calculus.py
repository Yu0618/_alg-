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
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
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
            raise SyntaxError("解析到空表達式")
        
        # 函數套用為左結合: e1 e2 e3 -> ((e1 e2) e3)
        res = exprs[0]
        for e in exprs[1:]:
            res = App(res, e)
        return res

    def parse_primary(self):
        kind, val = self.peek()
        if kind == 'LAMBDA':
            self.consume('LAMBDA')
            param = self.consume('VAR')
            self.consume('DOT')
            body = self.parse_expression()
            return Abs(param, body)
        elif kind == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        elif kind == 'VAR':
            name = self.consume('VAR')
            # 若變數名在環境中有定義巨集，則直接展開
            if name in self.env:
                return self.env[name]
            return Var(name)
        else:
            raise SyntaxError(f"無法識別的語法開頭: {kind} ({val})")


# ==========================================
# 3. 變數替換與 alpha-conversion
# ==========================================

def get_free_variables(node):
    """取得語法樹中所有的自由變數名稱集合"""
    if isinstance(node, Var):
        return {node.name}
    elif isinstance(node, Abs):
        return get_free_variables(node.body) - {node.param}
    elif isinstance(node, App):
        return get_free_variables(node.fn) | get_free_variables(node.arg)
    return set()

def substitute(node, var_name, replacement):
    """
    代換操作: node[var_name := replacement]
    具備 α-conversion 換名機制，防止變數捕捉
    """
    if isinstance(node, Var):
        return replacement if node.name == var_name else node

    elif isinstance(node, Abs):
        # 1. 被參數遮蔽，無需替換
        if node.param == var_name:
            return node
        
        free_in_repl = get_free_variables(replacement)
        # 2. 避免捕捉自由變數：若抽象參數出現在 replacement 的自由變數中，進行 α-conversion 重新命名
        if node.param in free_in_repl:
            new_param = node.param + "'"
            while new_param in free_in_repl or new_param in get_free_variables(node.body):
                new_param += "'"
            # 將舊參數換成新參數
            renamed_body = substitute(node.body, node.param, Var(new_param))
            return Abs(new_param, substitute(renamed_body, var_name, replacement))
        else:
            return Abs(node.param, substitute(node.body, var_name, replacement))

    elif isinstance(node, App):
        return App(substitute(node.fn, var_name, replacement), 
                   substitute(node.arg, var_name, replacement))


# ==========================================
# 4. β-Reduction（單步與完整過程化簡）
# ==========================================

def reduce_step(node, strategy='normal'):
    """
    對 AST 執行『單一步驟』的 β-reduction
    回傳元組: (reduced_node, stepped_boolean, description_str)
    """
    if strategy == 'normal': # 正規順序：最左外層優先
        if isinstance(node, App):
            # 找到 Redex: (λx. M) N
            if isinstance(node.fn, Abs):
                redex_str = f"({node.fn} {node.arg})"
                reduced = substitute(node.fn.body, node.fn.param, node.arg)
                return reduced, True, f"β-歸約化簡: {redex_str}  ==>  代入 {node.fn.param}"
            
            # 否則先規約左子樹
            new_fn, stepped, desc = reduce_step(node.fn, strategy)
            if stepped:
                return App(new_fn, node.arg), True, desc
            
            # 再規約右子樹
            new_arg, stepped, desc = reduce_step(node.arg, strategy)
            if stepped:
                return App(node.fn, new_arg), True, desc

        elif isinstance(node, Abs):
            new_body, stepped, desc = reduce_step(node.body, strategy)
            if stepped:
                return Abs(node.param, new_body), True, desc

    return node, False, ""

def evaluate(node, max_steps=50, strategy='normal'):
    """執行完整計算流程並輸出詳細步驟"""
    current = node
    print(f"  [步驟 0] 初始狀態: {current}")
    
    for step in range(1, max_steps + 1):
        current, stepped, desc = reduce_step(current, strategy)
        if not stepped:
            print(f"  └─► 計算完成 (達正則形式 Normal Form): {current}\n")
            return current
        print(f"  [步驟 {step}] {desc}")
        print(f"          目前結果: {current}")
    
    print(f"  └─► 已達到最大步驟上限 ({max_steps})，可能存在發散（如 Ω Combinator）。\n")
    return current


# ==========================================
# 5. De Bruijn Index 無名稱表示法轉換
# ==========================================

def to_debruijn(node, env=None):
    """將具名 AST 轉為 De Bruijn 指標表示法"""
    if env is None:
        env = []
    
    if isinstance(node, Var):
        if node.name in env:
            # 索引代表離綁定它的 λ 有幾層
            index = env.index(node.name) + 1
            return str(index)
        return node.name # 自由變數保持原名
    
    elif isinstance(node, Abs):
        # 進入 λ，將參數加到環境最前端
        return f"(λ {to_debruijn(node.body, [node.param] + env)})"
    
    elif isinstance(node, App):
        return f"({to_debruijn(node.fn, env)} {to_debruijn(node.arg, env)})"


# ==========================================
# 6. 範例展示與主程式
# ==========================================

def parse_expr(code, env=None):
    tokens = tokenize(code)
    return Parser(tokens, env).parse()

if __name__ == "__main__":
    print("=" * 60)
    print("      Lambda Calculus 步驟解譯器 (Python 版)")
    print("=" * 60 + "\n")

    # 定義常用的 Lambda 巨集庫 ( Church Encodings )
    env = {}
    
    # 布林值
    env['TRUE']  = parse_expr(r"\x.\y.x")
    env['FALSE'] = parse_expr(r"\x.\y.y")
    env['AND']   = parse_expr(r"\p.\q.p q p")
    
    # 邱奇數 (Church Numerals)
    env['ZERO']  = parse_expr(r"\f.\x.x")
    env['ONE']   = parse_expr(r"\f.\x.f x")
    env['TWO']   = parse_expr(r"\f.\x.f (f x)")
    env['SUCC']  = parse_expr(r"\n.\f.\x.f (n f x)")
    env['PLUS']  = parse_expr(r"\m.\n.\f.\x.m f (n f x)")

    # 組合子
    env['I']     = parse_expr(r"\x.x")
    env['K']     = parse_expr(r"\x.\y.x")
    env['S']     = parse_expr(r"\x.\y.\z.x z (y z)")

    # 測試項目 1: 邏輯運算 (AND TRUE FALSE)
    print("【範例 1】邏輯運算: AND TRUE FALSE")
    expr1 = parse_expr("AND TRUE FALSE", env)
    print(f"De Bruijn 表示法: {to_debruijn(expr1)}")
    evaluate(expr1)

    # 測試項目 2: 邱奇數加法 (1 + 1)
    print("【範例 2】邱奇數加法: PLUS ONE ONE")
    expr2 = parse_expr("PLUS ONE ONE", env)
    print(f"De Bruijn 表示法: {to_debruijn(expr2)}")
    evaluate(expr2)

    # 測試項目 3: 換名（α-conversion）防捕捉測試
    print("【範例 3】α-conversion 防止變數捕捉測試: (\\x.\\y.x y) y")
    expr3 = parse_expr(r"(\x.\y.x y) y")
    print(f"De Bruijn 表示法: {to_debruijn(expr3)}")
    evaluate(expr3)
