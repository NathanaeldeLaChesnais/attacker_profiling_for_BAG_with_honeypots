import re

# Définir les types de tokens
TOKENS = [
    ('VAR', r'[a-zA-Z][a-zA-Z0-9.\-]*'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('AND', r'&'),
    ('OR', r'\|'),
    ('WS', r'\s+'),  # Ignore les espaces
]

def tokenizer(expression):
    tokens = []
    while expression:
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(expression)
            if match:
                if token_type != 'WS':  # Ignore les espaces
                    tokens.append((token_type, match.group(0)))
                expression = expression[match.end():]
                break
        if not match:
            raise SyntaxError(f'Unexpected character: {expression[0]}')
    return tokens

class ASTNode:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        self.children = []

    def ajouter_enfant(self, enfant):
        self.children.append(enfant)

    def __repr__(self):
        if not self.children:
            return f'{self.value}'
        else :
            return f'{self.children[0]}{self.value}{self.children[1]}'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type):
        token = self.current_token()
        if token and token[0] == expected_type:
            self.pos += 1
            return token
        raise SyntaxError(f'Expected {expected_type} but got {token}')

    def parse(self):
        return self.expression()

    def expression(self):
        node = self.term()
        while self.current_token() and self.current_token()[0] == 'OR':
            op = self.consume('OR')
            right = self.term()
            new_node = ASTNode('OR', op[1])
            new_node.ajouter_enfant(node)
            new_node.ajouter_enfant(right)
            node = new_node
        return node

    def term(self):
        node = self.factor()
        while self.current_token() and self.current_token()[0] == 'AND':
            op = self.consume('AND')
            right = self.factor()
            new_node = ASTNode('AND', op[1])
            new_node.ajouter_enfant(node)
            new_node.ajouter_enfant(right)
            node = new_node
        return node

    def factor(self):
        token = self.current_token()
        if token[0] == 'VAR':
            self.consume('VAR')
            return ASTNode('VAR', token[1])
        elif token[0] == 'LPAREN':
            self.consume('LPAREN')
            node = self.expression()
            self.consume('RPAREN')
            return node
        else:
            raise SyntaxError(f'Unexpected token: {token}')

        
def compile_ast(ast):
    print(ast.value)
    if ast.type == 'VAR':
        return ast.value
    elif ast.type in ('AND', 'OR'):
        left = compile_ast(ast.children[0])
        right = compile_ast(ast.children[1])
        return f'({left} {ast.value} {right})'
    else:
        raise ValueError(f'Unknown AST node type: {ast.type}')

# Exemple d'utilisation
expression = "Responder & ( impacket | Metasploit )"
tokens = tokenizer(expression)
print("Tokens:", tokens)

parser = Parser(tokens)
ast = parser.parse()
print("AST:", ast)

compiled_expression = compile_ast(ast)
print("Compiled Expression:", compiled_expression)