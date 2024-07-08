import re
import numpy as np
import csv
from pgmpy.factors.discrete import TabularCPD
from BAG_Code.createANDtable import create_AND_table
from BAG_Code.createORtable import create_OR_table

# Définir les types de tokens
TOKENS = [
    ('VAR', r'[a-zA-Z][a-zA-Z0-9.\-\_]*'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('AND', r'&'),
    ('OR', r'\|'),
    ('WS', r'\s+'),  # Ignore les espaces
]

def tokenizer(expression):
    """
    Tokenizes the given expression into a list of tokens.

    Args:
        expression (str): The expression to tokenize.

    Returns:
        list: A list of tuples representing the tokens, where each tuple contains the token type and the token value.

    Raises:
        SyntaxError: If an unexpected character is encountered in the expression.
    """
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
    """
    Represents a node in an Abstract Syntax Tree (AST).

    Attributes:
        type (str): The type of the node.
        value: The value associated with the node.
        children (list): The list of child nodes.
    """

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        self.children = []

    def ajouter_enfant(self, enfant):
        """
        Adds a child node to the current node.

        Args:
            enfant: The child node to be added.
        """
        self.children.append(enfant)

    def __repr__(self):
        """
        Returns a string representation of the node.

        If the node has no children, it returns the value of the node.
        Otherwise, it returns the concatenation of the string representations
        of the first child, the value of the node, and the string representation
        of the second child.
        """
        if not self.children:
            return f'{self.value}'
        else:
            return f'{self.children[0]}{self.value}{self.children[1]}'

class Parser:
    def __init__(self, tokens):
            """
            Initializes a new instance of the Parser class.

            Args:
                tokens (list): A list of tokens.

            Attributes:
                tokens (list): The list of tokens.
                pos (int): The current position in the list of tokens.
            """
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
    if ast.type == 'VAR':
        return ast.value
    elif ast.type in ('AND', 'OR'):
        left = compile_ast(ast.children[0])
        right = compile_ast(ast.children[1])
        return f'({left} {ast.value} {right})'
    else:
        raise ValueError(f'Unknown AST node type: {ast.type}')
    
def build_tools_tree_original(BAG, ast, id, ONE, kts_base_score):
    """
    Recursively builds a tools tree in the Bayesian network.

    Parameters:
    - BAG: The Bayesian network object to which the tools tree is being built.
    - ast: The current node in the abstract syntax tree (AST).
    - id: The identifier of the parent node in the tools tree.
    - ONE: A constant representing the value 1.
    - kts_base_score: A dictionary containing the base scores for each tool in the AST.

    Returns:
    None
    """
    if ast.type == 'AND':
        BAG.add_edge(ast.__repr__(), id)
        for child in ast.children:
            build_tools_tree_original(BAG, child, ast.__repr__(), ONE, kts_base_score)
        if BAG.get_cpds(ast.__repr__()) == None:
            BAG.add_cpds(TabularCPD(ast.__repr__(), 2, create_AND_table([ONE, ONE]).T, [child.__repr__() for child in ast.children], evidence_card=2*np.ones(len(ast.children))))
    elif ast.type == 'OR':
        BAG.add_edge(ast.__repr__(), id)
        for child in ast.children:
            build_tools_tree_original(BAG, child, ast.__repr__(), ONE, kts_base_score)
        if BAG.get_cpds(ast.__repr__()) == None:
            BAG.add_cpds(TabularCPD(ast.__repr__(), 2, create_OR_table([ONE, ONE]).T, [child.__repr__() for child in ast.children], evidence_card=2*np.ones(len(ast.children))))
    else:
        BAG.add_edge(ast.__repr__(), id)
        if BAG.get_cpds(ast.__repr__()) == None:
            BAG.add_cpds(TabularCPD(ast.__repr__(), 2, [[1 - kts_base_score[ast.__repr__()]], [kts_base_score[ast.__repr__()]]]))

def build_tools_tree_static(BAG, ast, id, ONE, kts_base_score):
    """
    Calculate the probabilities of the tools tree in the Bayesian network.

    Args:
        BAG: The BAG object.
        ast: The current node in the AST.
        id: The identifier of the current node.
        ONE: A constant value.
        kts_base_score: A dictionary containing base scores for different nodes.

    Returns:
        The probability of the tools tree.

    Raises:
        None.
    """
    if ast.type == 'AND':
        prob = 1
        for child in ast.children:
            prob = prob * build_tools_tree_static(BAG, child, ast.__repr__(), ONE, kts_base_score)
        return prob
    elif ast.type == 'OR':
        prod = 1        
        for child in ast.children:
            prod = prod * (1 - build_tools_tree_static(BAG, child, ast.__repr__(), ONE, kts_base_score))
        return 1 - prod
    else:
        return kts_base_score[ast.__repr__()]

def kts_layer_original(BAG, ONE, nodes):
    """
    Constructs the knowledge, tooling, and skills (KTS) layer of a Bayesian
    Network using the provided BAG object.

    Parameters:
    - BAG: The Bayesian Network object to which the KTS layer will be added.
    - ONE: A constant value representing the number 1.
    - nodes: A dictionary containing information about the nodes in the network.

    Returns:
    None
    """
    with open('./Threat_Inteligence/kts_base_score.csv', mode='r') as kts_basescore_file:
        reader = csv.DictReader(kts_basescore_file)
        kts_base_score = {}
        for row in reader:
            kts_base_score[row['kts']] = float(row['base_score'])

    # Import all the dependencies
    cpt_l4 = create_AND_table([ONE, ONE, ONE, ONE])
    with open('./Threat_Inteligence/CVE_knowledge_tooling_skills.csv', mode='r') as ktsfile:
        reader = csv.DictReader(ktsfile)
        kts_dict = {}
        for row in reader:
            cve = row['Vulnerability']
            tmp = {'tool': row['tool'], 'skills': row['skills'], 'knowledge': row['knowledge']}
            kts_dict[cve] = tmp
    for node in nodes.items():
            id = node[0]
            node = node[1]
            if node['CVE'] != "null":
                row = kts_dict[node['CVE']]
                build_tools_tree_original(BAG, Parser(tokenizer(row['tool'])).parse(), id, ONE, kts_base_score)
                build_tools_tree_original(BAG, Parser(tokenizer(row['skills'])).parse(), id, ONE, kts_base_score)
                build_tools_tree_original(BAG, Parser(tokenizer(row['knowledge'])).parse(), id, ONE, kts_base_score)
                parents = BAG.get_parents(id)
                BAG.remove_cpds(id)
                BAG.add_cpds(TabularCPD(id, 2, cpt_l4.T, parents, evidence_card=2*np.ones(len(parents))))

def kts_layer_static(BAG, ONE, nodes):
    with open('./Threat_Inteligence/kts_base_score.csv', mode='r') as kts_basescore_file:
        reader = csv.DictReader(kts_basescore_file)
        kts_base_score = {}
        for row in reader:
            kts_base_score[row['kts']] = float(row['base_score'])
    # The skills layer:
    cpd_Lskills = TabularCPD('Lskills', 2, [[1-kts_base_score['L']], [kts_base_score['L']]])
    cpd_Hskills = TabularCPD('Hskills', 2, [[1-kts_base_score['H']], [kts_base_score['H']]])
    
    # The knowledge layer:
    cpd_knowledge = [TabularCPD(knowledge, 2, [[0.3], [0.7]]) for knowledge in ['Known vulnerabilities', 'CQCM', 'No credentials', 'MITM', 'Permissions move', 'Privilege escalation', 'Lateral move', 'ADCS']]

    # Import all the dependencies
    cpt_l4 = create_AND_table([ONE, ONE, ONE, ONE])
    with open('./Threat_Inteligence/CVE_knowledge_tooling_skills.csv', mode='r') as ktsfile:
        reader = csv.DictReader(ktsfile)
        kts_dict = {}
        for row in reader:
            cve = row['Vulnerability']
            tmp = {'tool': row['tool'], 'skills': row['skills'], 'knowledge': row['knowledge']}
            kts_dict[cve] = tmp
    for node in nodes.items():
            id = node[0]
            node = node[1]
            if node['CVE'] != "null":
                row = kts_dict[node['CVE']]
                tool_score = build_tools_tree_static(BAG, Parser(tokenizer(row['tool'])).parse(), id, ONE, kts_base_score)
                skills_score = kts_base_score[row['skills']]
                k_score = build_tools_tree_static(BAG, Parser(tokenizer(row['knowledge'])).parse(), id, ONE, kts_base_score)
                prob = tool_score * skills_score * k_score
                prob = prob + 0.01 - prob*0.01
                cpt_l4 = [[1, 1-prob], [0, prob]]
                parents = BAG.get_parents(id)
                BAG.remove_cpds(id)
                BAG.add_cpds(TabularCPD(id, 2, cpt_l4, parents, evidence_card=2*np.ones(len(parents))))
    # We add all the necessary CPDs to the BAG
    for cpd in [cpd_Lskills, cpd_Hskills] + cpd_knowledge:
        if BAG.__contains__(cpd.variable):
            BAG.add_cpds(cpd)

# Exemple d'utilisation
if __name__ == '__main__':
    expression = "Responder & ( impacket | Metasploit )"
    tokens = tokenizer(expression)
    print("Tokens:", tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)

    compiled_expression = compile_ast(ast)
    print("Compiled Expression:", compiled_expression)