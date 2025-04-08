# AQL (ATS Query Language) Documentation

## Overview
AQL is a domain-specific language designed for querying candidate data with a simple and intuitive syntax. It provides a flexible way to express complex filtering conditions using logical operators and comparisons.

## Abstract Syntax Tree (AST)

The AST represents the structure of AQL queries using the following node types:

### Core Node Types
- `Query`: Root node of the AST
- `LogicalExpression`: Represents logical operations (AND, OR, NOT)
- `ComparisonCondition`: Represents field comparisons
- `Identifier`: Represents field names (e.g., YOE, SKILLS)
- `Value`: Represents literal values (numbers, strings, booleans)
- `SetLiteral`: Represents a set of values for IN operations

### Operators

#### Comparison Operators
- `EQUALS` (=)
- `NOT_EQUALS` (!=)
- `GREATER_THAN` (>)
- `LESS_THAN` (<)
- `GREATER_EQUAL` (>=)
- `LESS_EQUAL` (<=)
- `IN` (IN)

#### Logical Operators
- `AND`
- `OR`
- `NOT`

## Supported Queries

### Basic Comparisons
```aql
YOE > 5
LOCATION = 'San Francisco'
SKILLS != 'Java'
```

### Set Operations
```aql
SKILLS IN {'Python', 'Java', 'JavaScript'}
```

### Logical Combinations
```aql
YOE >= 3 AND SKILLS IN {'ReactJS', 'NodeJS'}
LOCATION = 'San Francisco' AND (YOE > 5 OR SKILLS IN {'Rust', 'Go'})
```

### Negation
```aql
NOT SKILLS = 'Java'
```

## Query Examples

1. Find candidates with more than 5 years of experience:
   ```aql
   YOE > 5
   ```

2. Find candidates in San Francisco with specific skills:
   ```aql
   LOCATION = 'San Francisco' AND SKILLS IN {'Python', 'JavaScript'}
   ```

3. Find candidates with either significant experience or specific skills:
   ```aql
   YOE >= 8 OR SKILLS IN {'Rust', 'Go'}
   ```

4. Find candidates who don't have Java skills:
   ```aql
   NOT SKILLS = 'Java'
   ```

## Implementation Details

The AQL implementation consists of three main components:

1. **Lexer**: Tokenizes the input query string
2. **Parser**: Converts tokens into an AST
3. **Query Translator**: Converts the AST into executable SQL queries

The system supports:
- Numeric comparisons
- String comparisons
- Boolean values
- Set operations
- Complex logical expressions with parentheses
- Field-based filtering

## Error Handling

The system provides detailed error messages for:
- Invalid syntax
- Unclosed parentheses
- Invalid operators
- Malformed set literals
- Unexpected tokens
