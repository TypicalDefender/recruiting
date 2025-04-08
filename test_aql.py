from aql import parse, print_ast, LexerError, ParserError

def test_query(query_str: str):
    print(f"\nTesting query: {query_str}")
    print("-" * 50)
    try:
        ast = parse(query_str)
        print("Parsed AST:")
        print_ast(ast)
    except (LexerError, ParserError) as e:
        print(f"Error: {e}")
    print("-" * 50)

def main():
    # Basic queries
    test_query("YOE > 5")
    test_query("SKILLS IN {'Python', 'Java', 'SQL'}")
    
    # Compound queries with AND/OR
    test_query("YOE >= 3 AND SKILLS IN {'ReactJS', 'NodeJS'}")
    test_query("LOCATION = 'San Francisco' OR LOCATION = 'New York'")
    
    # Complex nested queries
    test_query("LOCATION = 'San Francisco' AND (YOE > 5 OR SKILLS IN {'Rust', 'Go'})")
    test_query("(YOE > 3 AND SKILLS IN {'Python'}) OR (YOE > 5 AND SKILLS IN {'Java'})")
    
    # Different comparison operators
    test_query("SALARY >= 100000")
    test_query("EXPERIENCE != 'Entry Level'")
    test_query("EDUCATION = 'Bachelor Degree'")
    
    # Multiple skill requirements
    test_query("SKILLS IN {'AWS', 'Docker', 'Kubernetes'} AND YOE >= 4")
    
    # Testing error cases
    print("\nTesting error cases:")
    print("-" * 50)
    
    # Invalid operator
    test_query("YOE >> 5")  # Should fail - invalid operator
    
    # Missing closing brace
    test_query("SKILLS IN {'Python', 'Java'")  # Should fail - unclosed brace
    
    # Invalid identifier
    test_query("invalid_field > 5")  # Should fail - lowercase identifier
    
    # Missing value
    test_query("YOE >")  # Should fail - missing value
    
    # Invalid set syntax
    test_query("SKILLS IN {}")  # Empty set - should work
    test_query("SKILLS IN {,}")  # Should fail - invalid set syntax

if __name__ == "__main__":
    main() 