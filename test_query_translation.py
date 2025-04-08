from aql.db.query_translator import translate_query

def test_translation(query_str: str):
    print(f"\nAQL Query: {query_str}")
    print("-" * 50)
    try:
        sql, params = translate_query(query_str)
        print("SQL Query:")
        print(sql)
        print("\nParameters:", params)
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)

def main():
    # Test basic queries
    test_translation("YOE > 5")
    # test_translation("SKILLS IN {'Python', 'Java', 'SQL'}")
    
    # # Test compound queries with automatic join handling
    # test_translation("YOE >= 3 AND SKILLS IN {'ReactJS', 'NodeJS'}")
    # test_translation("LOCATION = 'San Francisco' OR LOCATION = 'New York'")
    
    # # Test complex nested queries
    # test_translation(
    #     "LOCATION = 'San Francisco' AND (YOE > 5 OR SKILLS IN {'Rust', 'Go'})"
    # )
    # test_translation(
    #     "(YOE > 3 AND SKILLS IN {'Python'}) OR (YOE > 5 AND SKILLS IN {'Java'})"
    # )
    
    # # Test different operators
    # test_translation("SALARY >= 100000")
    # test_translation("EXPERIENCE != 'Entry Level'")
    # test_translation("EDUCATION = 'Bachelor Degree'")
    
    # # Test multiple skill requirements
    # test_translation(
    #     "SKILLS IN {'AWS', 'Docker', 'Kubernetes'} AND YOE >= 4"
    # )
    
    # # Test queries that require multiple joins
    # test_translation(
    #     "SKILLS IN {'Python'} AND EDUCATION = 'Bachelor Degree'"
    # )

if __name__ == "__main__":
    main() 