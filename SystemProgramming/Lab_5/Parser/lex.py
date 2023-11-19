import ply.lex as lex

# Token list
tokens = (
    'NUMBER',  # for integers
    'PLUS',  # for +
    'MINUS',  # for -
    'TIMES',  # for *
    'DIVIDE',  # for /
    'LPAREN',  # for (
    'RPAREN',  # for )
    'EXPONENT',  # for ^
    'IDENTIFIER',
    'EQUALS',
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EXPONENT = r'\^'
# Regular expression rule for EQUALS
t_EQUALS = r'='


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)  # Change to float
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
