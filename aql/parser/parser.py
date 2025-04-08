from typing import List, Optional, Union
from .lexer import Token, TokenType, tokenize, LexerError
from .ast import (
    Node, Query, LogicalExpression, ComparisonCondition,
    Identifier, Value, SetLiteral,
    ComparisonOperator, LogicalOperator
)

class ParserError(Exception):
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        position_info = f" at position {token.position}" if token else ""
        super().__init__(f"{message}{position_info}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> Query:
        """Parse the tokens into an AST"""
        expression = self.parse_expression()
        if not self.is_at_end():
            raise ParserError("Expected end of input", self.peek())
        return Query(expression)
    
    def parse_expression(self) -> Node:
        """Parse a logical expression or condition"""
        expr = self.parse_condition()
        
        while (
            self.match(TokenType.AND) or 
            self.match(TokenType.OR)
        ):
            operator = LogicalOperator.AND if self.previous().type == TokenType.AND else LogicalOperator.OR
            right = self.parse_condition()
            expr = LogicalExpression(operator=operator, left=expr, right=right)
        
        return expr
    
    def parse_condition(self) -> Node:
        """Parse a comparison condition"""
        if self.match(TokenType.NOT):
            expr = self.parse_condition()
            return LogicalExpression(operator=LogicalOperator.NOT, left=expr)
        
        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        # Parse identifier
        if not self.match(TokenType.IDENTIFIER):
            raise ParserError("Expected identifier", self.peek())
        identifier = Identifier(self.previous().value)
        
        # Parse operator
        operator = self.parse_operator()
        
        # Parse value or set literal
        value = self.parse_value()
        
        return ComparisonCondition(
            field=identifier,
            operator=operator,
            value=value
        )
    
    def parse_operator(self) -> ComparisonOperator:
        """Parse a comparison operator"""
        if self.match(TokenType.EQUALS):
            return ComparisonOperator.EQUALS
        elif self.match(TokenType.NOT_EQUALS):
            return ComparisonOperator.NOT_EQUALS
        elif self.match(TokenType.GREATER_THAN):
            return ComparisonOperator.GREATER_THAN
        elif self.match(TokenType.LESS_THAN):
            return ComparisonOperator.LESS_THAN
        elif self.match(TokenType.GREATER_EQUAL):
            return ComparisonOperator.GREATER_EQUAL
        elif self.match(TokenType.LESS_EQUAL):
            return ComparisonOperator.LESS_EQUAL
        elif self.match(TokenType.IN):
            return ComparisonOperator.IN
        else:
            raise ParserError("Expected comparison operator", self.peek())
    
    def parse_value(self) -> Union[Value, SetLiteral]:
        """Parse a value or set literal"""
        if self.match(TokenType.LBRACE):
            return self.parse_set_literal()
        
        if self.match(TokenType.NUMBER):
            # Convert string to number
            try:
                value = float(self.previous().value)
                if value.is_integer():
                    value = int(value)
                return Value(value)
            except ValueError:
                raise ParserError("Invalid number", self.previous())
        
        if self.match(TokenType.STRING):
            # Remove quotes
            value = self.previous().value[1:-1]
            return Value(value)
        
        if self.match(TokenType.BOOLEAN):
            value = self.previous().value.upper() == "TRUE"
            return Value(value)
        
        raise ParserError("Expected value", self.peek())
    
    def parse_set_literal(self) -> SetLiteral:
        """Parse a set literal like {'value1', 'value2'}"""
        values = []
        
        # Handle empty set
        if self.match(TokenType.RBRACE):
            return SetLiteral(values)
        
        while True:
            if self.is_at_end():
                raise ParserError("Unclosed set literal - expected '}'")
            
            if self.match(TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN):
                token = self.previous()
                if token.type == TokenType.STRING:
                    values.append(Value(token.value[1:-1]))
                elif token.type == TokenType.NUMBER:
                    try:
                        value = float(token.value)
                        if value.is_integer():
                            value = int(value)
                        values.append(Value(value))
                    except ValueError:
                        raise ParserError("Invalid number in set", token)
                else:  # BOOLEAN
                    values.append(Value(token.value.upper() == "TRUE"))
            else:
                raise ParserError("Expected value in set", self.peek())
            
            if self.is_at_end():
                raise ParserError("Unclosed set literal - expected '}'")
            
            if self.match(TokenType.RBRACE):
                break
            
            if not self.match(TokenType.COMMA):
                raise ParserError("Expected ',' between values or '}' to close set", self.peek())
        
        return SetLiteral(values)
    
    # Helper methods
    def match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def check(self, type: TokenType) -> bool:
        """Check if current token is of given type without advancing"""
        if self.is_at_end():
            return False
        return self.peek().type == type
    
    def advance(self) -> Token:
        """Move to next token and return previous"""
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self) -> bool:
        """Check if we've reached end of tokens"""
        return self.current >= len(self.tokens)
    
    def peek(self) -> Token:
        """Return current token without advancing"""
        if self.is_at_end():
            raise ParserError("Unexpected end of input")
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        """Return previous token"""
        if self.current <= 0:
            raise ParserError("No previous token")
        return self.tokens[self.current - 1]
    
    def consume(self, type: TokenType, message: str) -> Token:
        """Consume token of expected type or raise error"""
        if self.check(type):
            return self.advance()
        raise ParserError(message, self.peek())

def parse(query: str) -> Query:
    """Helper function to tokenize and parse a query string"""
    try:
        tokens = tokenize(query)
        parser = Parser(tokens)
        return parser.parse()
    except LexerError as e:
        raise ParserError(str(e))

if __name__ == "__main__":
    # Test the parser with sample queries
    test_queries = [
        "YOE > 5",
        "SKILLS IN {'Python', 'Java'}",
        "YOE >= 3 AND SKILLS IN {'ReactJS', 'NodeJS'}",
        "LOCATION = 'San Francisco' AND (YOE > 5 OR SKILLS IN {'Rust', 'Go'})"
    ]
    
    from .ast import print_ast
    
    for query in test_queries:
        print(f"\nParsing query: {query}")
        try:
            ast = parse(query)
            print("AST:")
            print_ast(ast)
        except (LexerError, ParserError) as e:
            print(f"Error: {e}") 