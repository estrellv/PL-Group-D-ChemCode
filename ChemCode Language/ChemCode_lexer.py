import ply.lex as lex


#----------------------------
#List of token names
#----------------------------
tokens = [

    'FLOAT',
    'INT',
    'TEXT',
    'EQUALS',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'LANGLEBRA',
    'RANGLEBRA',
    'LPAR',
    'RPAR',
    'COMMA',
    'DISCOVER'

]

#Set tokens representation
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS= r'\='
t_LANGLEBRA = r'\<'
t_RANGLEBRA = r'\>'
t_LPAR = r'\('
t_RPAR = r'\)'
t_COMMA = r'\,'

t_ignore = " \t" # A string containing ignored characters (spaces and tabs)


def t_DISCOVER(t):
    r'discover'
    t.type = 'DISCOVER'
    return t

def t_TEXT(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'

    t.type = 'TEXT'
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# ------------------------------------------------------------
# Regular expression rule for error handling.
# ------------------------------------------------------------
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# ------------------------------------------------------------
# Build the lexer
# ------------------------------------------------------------
lexer = lex.lex()