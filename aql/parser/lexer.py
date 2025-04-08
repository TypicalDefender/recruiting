import re
from dataclasses import dataclass
from typing import List, Optional
from .grammar.aql_grammar import TokenType, PATTERNS

@dataclass
class Token:
    type: TokenType
    value: str
    position: int

class LexerError(Exception):
    def __init__(self, message: str, position: int):
        self.message = message
        self.position = position
        super().__init__(f"{message} at position {position}")

class Lexer:
    def __init__(self):
        # Combine all patterns into a single regex
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in PATTERNS.items())
        self.pattern = re.compile(self.token_regex)
        
    def tokenize(self, text: str) -> List[Token]:
        tokens = []
        position = 0
        
        while position < len(text):
            match = self.pattern.match(text, position)
            if match is None:
                raise LexerError(f"Invalid character sequence", position)
            
            position = match.end()
            
            # Get the name of the matched pattern
            token_type = match.lastgroup
            value = match.group()
            
            # Skip whitespace
            if token_type == 'WHITESPACE':
                continue
                
            # Convert string token type to enum
            try:
                token_enum = TokenType[token_type]
            except KeyError:
                raise LexerError(f"Unknown token type: {token_type}", position)
            
            tokens.append(Token(token_enum, value, position - len(value)))
        
        return tokens

def tokenize(query: str) -> List[Token]:
    """Helper function to tokenize a query string."""
    lexer = Lexer()
    return lexer.tokenize(query)

# Example usage:
if __name__ == "__main__":
    # Test the lexer with a sample query
    query = "YOE > 5 AND SKILLS IN {'ReactJS', 'NodeJS'}"
    try:
        tokens = tokenize(query)
        for token in tokens:
            print(f"Token(type={token.type}, value='{token.value}', pos={token.position})")
    except LexerError as e:
        print(f"Error: {e}") 