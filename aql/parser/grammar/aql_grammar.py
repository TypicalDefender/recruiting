from enum import Enum, auto

class TokenType(Enum):
    # Operators
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Comparisons
    EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    IN = auto()
    
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    
    # Special
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    IDENTIFIER = auto()

# Grammar Rules in EBNF notation:
"""
# Top level query
query := expression

# Expression can be a single condition or multiple conditions joined by logical operators
expression := condition
            | expression AND expression
            | expression OR expression
            | NOT expression
            | '(' expression ')'

# Basic conditions for resume filtering
condition := identifier comparison_op value
           | identifier IN set_literal

# Comparison operators
comparison_op := '=' | '!=' | '>' | '<' | '>=' | '<='

# Value types
value := number | string | boolean

# Set literal for IN operations
set_literal := '{' value_list '}'
value_list := value (',' value)*

# Identifiers (field names)
identifier := 'YOE' | 'SKILLS' | 'EDUCATION' | 'EXPERIENCE' | 'LOCATION' | ...

Examples:
YOE > 5
SKILLS IN {'Python', 'Java', 'SQL'}
YOE >= 3 AND SKILLS IN {'ReactJS', 'NodeJS'}
LOCATION = 'San Francisco' AND (YOE > 5 OR SKILLS IN {'Rust', 'Go'})
"""

# Token patterns (to be used with lexer)
PATTERNS = {
    'AND': r'AND\b',
    'OR': r'OR\b',
    'NOT': r'NOT\b',
    'IN': r'IN\b',
    'NUMBER': r'\d+(\.\d*)?',
    'STRING': r"'[^']*'|\"[^\"]*\"",
    'BOOLEAN': r'TRUE|FALSE',
    'IDENTIFIER': r'[A-Z][A-Z_]*\b',
    'GREATER_EQUAL': r'>=',
    'LESS_EQUAL': r'<=',
    'EQUALS': r'=',
    'NOT_EQUALS': r'!=',
    'GREATER_THAN': r'>',
    'LESS_THAN': r'<',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'LBRACE': r'\{',
    'RBRACE': r'\}',
    'COMMA': r',',
    'WHITESPACE': r'[ \t\n]+',  # Ignored
} 