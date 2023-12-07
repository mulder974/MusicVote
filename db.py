import os
import psycopg2
from psycopg2 import sql
import security


# Establish a connection to the database
conn = psycopg2.connect("postgresql://mulder974:nghtIMk7xrP3@ep-autumn-cake-33374612.eu-central-1.aws.neon.tech/PubSong?sslmode=require")
cursor = conn.cursor()

# SQL to create a table (run this once)
create_table_query = """
CREATE TABLE IF NOT EXISTS tokens (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255) UNIQUE NOT NULL
);
"""
cursor.execute(create_table_query)
conn.commit()

# Function to generate tokens
def generate_tokens(n):
    tokens = []
    for e in range(0, n):
        token = security.generate_token(16)
        tokens.append(token)
    return tokens

# Function to insert tokens into the database
def insert_tokens(tokens):
    for token in tokens:
        insert_query = sql.SQL("INSERT INTO tokens (token) VALUES (%s) ON CONFLICT DO NOTHING;")
        cursor.execute(insert_query, (token,))
    conn.commit()

# Generate and insert 10 tokens
tokens = generate_tokens(10)
insert_tokens(tokens)

# Close the connection
cursor.close()
conn.close()