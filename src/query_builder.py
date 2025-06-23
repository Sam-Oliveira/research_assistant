"""
Process user input to build an arXiv search query.
Valid keys: topic, title, author, category.
"""

def field_pair(field: str, value: str) -> str:
    mapping = {"topic": "all", "title": "ti", "author": "au", "category": "cat"}
    prefix  = mapping[field]            
    value   = value.replace('"', '')
    return f'{prefix}:"{value}"'

def build_query(**kwargs) -> str:
    parts = [field_pair(k, v) for k, v in kwargs.items() if v]
    return " AND ".join(f"({p})" for p in parts) or "all:*"