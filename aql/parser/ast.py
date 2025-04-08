from dataclasses import dataclass
from typing import List, Union, Optional
from enum import Enum, auto

class ComparisonOperator(Enum):
    EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    IN = auto()

class LogicalOperator(Enum):
    AND = auto()
    OR = auto()
    NOT = auto()

@dataclass
class Node:
    """Base class for all AST nodes"""
    pass

@dataclass
class Value(Node):
    """Represents a literal value (number, string, boolean)"""
    value: Union[int, float, str, bool]

@dataclass
class SetLiteral(Node):
    """Represents a set of values, used with IN operator"""
    values: List[Value]

@dataclass
class Identifier(Node):
    """Represents a field name (e.g., YOE, SKILLS)"""
    name: str

@dataclass
class ComparisonCondition(Node):
    """Represents a comparison between a field and a value"""
    field: Identifier
    operator: ComparisonOperator
    value: Union[Value, SetLiteral]

@dataclass
class LogicalExpression(Node):
    """Represents a logical operation (AND, OR, NOT)"""
    operator: LogicalOperator
    left: Node
    right: Optional[Node] = None  # Right is None for NOT operations

@dataclass
class Query(Node):
    """Root node of the AST"""
    expression: Node

# Example of building an AST for: YOE > 5 AND SKILLS IN {'ReactJS', 'NodeJS'}
def create_example_ast() -> Query:
    yoe_condition = ComparisonCondition(
        field=Identifier("YOE"),
        operator=ComparisonOperator.GREATER_THAN,
        value=Value(5)
    )
    
    skills_condition = ComparisonCondition(
        field=Identifier("SKILLS"),
        operator=ComparisonOperator.IN,
        value=SetLiteral([Value("ReactJS"), Value("NodeJS")])
    )
    
    return Query(
        expression=LogicalExpression(
            operator=LogicalOperator.AND,
            left=yoe_condition,
            right=skills_condition
        )
    )

# Helper functions for AST manipulation
def visit_ast(node: Node, visitor_fn):
    """Traverse the AST and apply visitor_fn to each node"""
    visitor_fn(node)
    
    if isinstance(node, LogicalExpression):
        visit_ast(node.left, visitor_fn)
        if node.right:
            visit_ast(node.right, visitor_fn)
    elif isinstance(node, ComparisonCondition):
        visit_ast(node.field, visitor_fn)
        visit_ast(node.value, visitor_fn)
    elif isinstance(node, SetLiteral):
        for value in node.values:
            visit_ast(value, visitor_fn)
    elif isinstance(node, Query):
        visit_ast(node.expression, visitor_fn)

def print_ast(node: Node, level: int = 0):
    """Pretty print the AST"""
    indent = "  " * level
    if isinstance(node, Query):
        print(f"{indent}Query")
        print_ast(node.expression, level + 1)
    elif isinstance(node, LogicalExpression):
        print(f"{indent}LogicalExpression({node.operator})")
        print_ast(node.left, level + 1)
        if node.right:
            print_ast(node.right, level + 1)
    elif isinstance(node, ComparisonCondition):
        print(f"{indent}Comparison({node.operator})")
        print_ast(node.field, level + 1)
        print_ast(node.value, level + 1)
    elif isinstance(node, Identifier):
        print(f"{indent}Identifier({node.name})")
    elif isinstance(node, Value):
        print(f"{indent}Value({node.value})")
    elif isinstance(node, SetLiteral):
        print(f"{indent}Set({[v.value for v in node.values]})")

if __name__ == "__main__":
    # Test AST creation and printing
    ast = create_example_ast()
    print("Example AST for: YOE > 5 AND SKILLS IN {'ReactJS', 'NodeJS'}")
    print_ast(ast) 