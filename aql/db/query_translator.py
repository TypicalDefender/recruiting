from typing import List, Dict, Any, Tuple
from ..parser.ast import (
    Node, Query, LogicalExpression, ComparisonCondition,
    Identifier, Value, SetLiteral,
    ComparisonOperator, LogicalOperator
)
from .sql_builder import AQLQueryBuilder, Operators

class QueryTranslator:
    def __init__(self):
        # Mapping of AQL operators to SQL operator functions
        self.operator_mappings = {
            ComparisonOperator.EQUALS: Operators.equals,
            ComparisonOperator.NOT_EQUALS: Operators.not_equals,
            ComparisonOperator.GREATER_THAN: Operators.greater_than,
            ComparisonOperator.LESS_THAN: Operators.less_than,
            ComparisonOperator.GREATER_EQUAL: Operators.greater_equal,
            ComparisonOperator.LESS_EQUAL: Operators.less_equal,
            ComparisonOperator.IN: Operators.in_list
        }
    
    def translate(self, ast: Query) -> Tuple[str, List[Any]]:
        """
        Translate an AQL AST into a SQL query with parameters
        Returns: (query_string, parameters)
        """
        params: List[Any] = []
        builder = AQLQueryBuilder()
        
        # Translate the expression and add it to the builder
        criterion = self._translate_node(ast.expression, builder, params)
        builder.add_where(criterion)
        
        return builder.build(), params
    
    def _translate_node(self, node: Node, builder: AQLQueryBuilder, params: List[Any]):
        """Recursively translate an AST node into a SQL condition"""
        if isinstance(node, LogicalExpression):
            return self._translate_logical_expression(node, builder, params)
        elif isinstance(node, ComparisonCondition):
            return self._translate_comparison(node, builder, params)
        else:
            raise ValueError(f"Unexpected node type: {type(node)}")
    
    def _translate_logical_expression(self, expr: LogicalExpression, builder: AQLQueryBuilder, params: List[Any]):
        """Translate a logical expression (AND/OR/NOT) to SQL"""
        if expr.operator == LogicalOperator.NOT:
            right_criterion = self._translate_node(expr.left, builder, params)
            return ~right_criterion
        
        left_criterion = self._translate_node(expr.left, builder, params)
        right_criterion = self._translate_node(expr.right, builder, params)
        
        if expr.operator == LogicalOperator.AND:
            return left_criterion & right_criterion
        else:  # OR
            return left_criterion | right_criterion
    
    def _translate_comparison(self, condition: ComparisonCondition, builder: AQLQueryBuilder, params: List[Any]):
        """Translate a comparison condition to SQL"""
        field = builder.get_field(condition.field.name)
        operator = condition.operator
        value = condition.value
        
        if operator not in self.operator_mappings:
            raise ValueError(f"Unknown operator: {operator}")
        
        operator_func = self.operator_mappings[operator]
        
        # Handle values
        if isinstance(value, Value):
            params.append(value.value)
            return operator_func(field, params[-1])
        elif isinstance(value, SetLiteral):
            values = [v.value for v in value.values]
            params.extend(values)
            return operator_func(field, values)
        else:
            raise ValueError(f"Unexpected value type: {type(value)}")

def translate_query(query_str: str) -> Tuple[str, List[Any]]:
    """Helper function to parse and translate an AQL query to SQL"""
    from ..parser.parser import parse
    
    ast = parse(query_str)
    translator = QueryTranslator()
    return translator.translate(ast)

if __name__ == "__main__":
    # Test the translator with some sample queries
    test_queries = [
        "YOE > 5",
        "SKILLS IN {'Python', 'Java'}",
        "YOE >= 3 AND SKILLS IN {'ReactJS', 'NodeJS'}",
        "LOCATION = 'San Francisco' AND (YOE > 5 OR SKILLS IN {'Rust', 'Go'})"
    ]
    
    for query in test_queries:
        print(f"\nAQL Query: {query}")
        try:
            sql, params = translate_query(query)
            print("SQL Query:")
            print(sql)
            print("Parameters:", params)
        except Exception as e:
            print(f"Error: {e}") 