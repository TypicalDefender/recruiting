from typing import List, Any, Optional, Union
from pypika import Query, Table, Field, Order, JoinType
from pypika.queries import QueryBuilder
from pypika.terms import Criterion, Function, ValueWrapper

class AQLQueryBuilder:
    def __init__(self):
        # Define our main tables
        self.resumes = Table('resumes')
        self.skills = Table('skills')
        self.resume_skills = Table('resume_skills')
        self.education = Table('education')
        self.work_experience = Table('work_experience')
        self.projects = Table('projects')
        self.certifications = Table('certifications')
        
        # Start with base query
        self.query = Query.from_(self.resumes).select(self.resumes.star)
        
        # Track which joins we've already added
        self.added_joins = set()
    
    def add_join_if_needed(self, field: str) -> None:
        """Add necessary joins based on the field being queried"""
        if field.startswith('SKILLS'):
            if 'skills' not in self.added_joins:
                self.query = (
                    self.query
                    .left_join(self.resume_skills)
                    .on(self.resumes.id == self.resume_skills.resume_id)
                    .left_join(self.skills)
                    .on(self.resume_skills.skill_id == self.skills.id)
                )
                self.added_joins.add('skills')
        
        elif field.startswith('EDUCATION'):
            if 'education' not in self.added_joins:
                self.query = (
                    self.query
                    .left_join(self.education)
                    .on(self.resumes.id == self.education.resume_id)
                )
                self.added_joins.add('education')
        
        elif field.startswith('EXPERIENCE'):
            if 'work_experience' not in self.added_joins:
                self.query = (
                    self.query
                    .left_join(self.work_experience)
                    .on(self.resumes.id == self.work_experience.resume_id)
                )
                self.added_joins.add('work_experience')
    
    def get_field(self, field_name: str) -> Field:
        """Get the appropriate field based on the AQL field name"""
        field_mappings = {
            'YOE': self.resumes.years_of_experience,
            'LOCATION': self.resumes.location,
            'SALARY': self.resumes.current_salary,
            'EXPERIENCE': self.resumes.experience_level,
            'EDUCATION': self.education.degree,
            'SKILLS': self.skills.name
        }
        
        if field_name not in field_mappings:
            raise ValueError(f"Unknown field: {field_name}")
            
        self.add_join_if_needed(field_name)
        return field_mappings[field_name]
    
    def add_where(self, criterion: Criterion) -> 'AQLQueryBuilder':
        """Add a WHERE clause to the query"""
        self.query = self.query.where(criterion)
        return self
    
    def add_and(self, criterion: Criterion) -> 'AQLQueryBuilder':
        """Add an AND clause to the query"""
        self.query = self.query & criterion
        return self
    
    def add_or(self, criterion: Criterion) -> 'AQLQueryBuilder':
        """Add an OR clause to the query"""
        self.query = self.query | criterion
        return self
    
    def build(self) -> str:
        """Build and return the final SQL query"""
        return str(self.query)

class Operators:
    @staticmethod
    def equals(field: Field, value: Any) -> Criterion:
        return field == value
    
    @staticmethod
    def not_equals(field: Field, value: Any) -> Criterion:
        return field != value
    
    @staticmethod
    def greater_than(field: Field, value: Any) -> Criterion:
        return field > value
    
    @staticmethod
    def less_than(field: Field, value: Any) -> Criterion:
        return field < value
    
    @staticmethod
    def greater_equal(field: Field, value: Any) -> Criterion:
        return field >= value
    
    @staticmethod
    def less_equal(field: Field, value: Any) -> Criterion:
        return field <= value
    
    @staticmethod
    def in_list(field: Field, values: List[Any]) -> Criterion:
        return field.isin(values)

# Example usage:
# builder = AQLQueryBuilder()
# field = builder.get_field('YOE')
# builder.add_where(Operators.greater_than(field, 5))
# sql = builder.build() 