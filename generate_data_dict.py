import re
import pandas as pd
from collections import defaultdict

def parse_sql(sql_content):
    # Regular expressions to match table and column definitions
    table_regex = re.compile(r'CREATE TABLE ([\w\.]+) \((.*?)\);', re.S)
    column_regex = re.compile(r'\n(\w+)\s+(\w+\(?\d*\)?)\s*(NOT NULL)?\s*(PRIMARY KEY)?\s*(UNIQUE)?\s*(,|\n|\))', re.S)
    foreign_key_regex = re.compile(r'FOREIGN KEY \((\w+)\) REFERENCES ([\w\.]+) ?\((\w+)\)', re.S)
    insert_regex = re.compile(r'INSERT INTO ([\w\.]+) \((.*?)\) VALUES \((.*?)\);', re.S)
    
    tables = {}
    foreign_keys = []
    examples = defaultdict(dict)
    
    for table_match in table_regex.finditer(sql_content):
        table_name = table_match.group(1)
        columns_str = table_match.group(2)
        
        columns = []
        for column_match in column_regex.finditer(columns_str):
            column_name = column_match.group(1)
            data_type = column_match.group(2)
            required = 'Y' if column_match.group(3) else 'N'
            primary_key = 'Y' if column_match.group(4) else 'N'
            unique = 'Y' if column_match.group(5) else 'N'
            
            columns.append({
                'column_name': column_name,
                'data_type': data_type,
                'required': required,
                'unique': unique,
                'primary_key': primary_key,
                'foreign_key': 'N',
                'foreign_key_table': '',
                'foreign_key_column': ''
            })
        
        # Check for foreign keys
        for foreign_key_match in foreign_key_regex.finditer(columns_str):
            fk_column = foreign_key_match.group(1)
            fk_table = foreign_key_match.group(2)
            fk_ref_column = foreign_key_match.group(3)
            
            foreign_keys.append({
                'table': table_name,
                'column': fk_column,
                'ref_table': fk_table,
                'ref_column': fk_ref_column
            })
        
        tables[table_name] = columns
    
    # Assign foreign keys to the respective columns
    for fk in foreign_keys:
        for column in tables[fk['table']]:
            if column['column_name'] == fk['column']:
                column['foreign_key'] = 'Y'
                column['foreign_key_table'] = fk['ref_table']
                column['foreign_key_column'] = fk['ref_column']
    
    # Extract example values from INSERT queries
    for insert_match in insert_regex.finditer(sql_content):
        table_name = insert_match.group(1)
        columns_str = insert_match.group(2)
        values_str = insert_match.group(3)
        
        columns = columns_str.split(', ')
        values = values_str.split(', ')
        
        for col, val in zip(columns, values):
            examples[table_name][col] = val.strip("'")
    
    return tables, examples

def singularize_and_titlecase(word):
    if word.endswith('s'):
        word = word[:-1]
    return word.title()

def create_data_dictionary(tables, examples):
    data = []
    for table_name, columns in tables.items():
        schema, table = table_name.split('.')
        example_dict = examples[table_name.lower()]
        for column in columns:
            example_value = example_dict.get(column['column_name'].lower(), 'Example Value')
            data.append([
                singularize_and_titlecase(table),
                schema,
                table,
                column['column_name'],
                column['data_type'],
                column['required'],
                column['unique'],
                f'Description for {column["column_name"]}',
                example_value,
                column['primary_key'],
                column['foreign_key'],
                column['foreign_key_table'],
                column['foreign_key_column']
            ])

    df = pd.DataFrame(data, columns=[
        "Entity", "Source System", "Table Name",
        "Column Name", "Data Type", "Required", "Unique",
        "Description", "Value Example", "Primary Key",
        "Foreign Key", "Foreign Key Table", "Foreign Key Column"
    ])
    
    return df

# Read SQL content from a file
file_path = 'sneakerpark.sql'
with open(file_path, 'r') as file:
    sql_content = file.read()

# Parse the SQL content to get table and column definitions and example values
tables, examples = parse_sql(sql_content)

# Create a data dictionary DataFrame
data_dictionary = create_data_dictionary(tables, examples)

# Display the data dictionary
print(data_dictionary["Value Example"])

# Optionally, save the data dictionary to a CSV file
data_dictionary.to_csv('data_dictionary.csv', index=False)