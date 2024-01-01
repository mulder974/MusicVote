import os
import psycopg2
from psycopg2 import sql
import security


postgresql_str = "postgresql://mulder974:nghtIMk7xrP3@ep-autumn-cake-33374612.eu-central-1.aws.neon.tech/PubSong?sslmode=require"

# Function to generate tokens
def generate_tokens(n):
    tokens = []
    for e in range(0, n):
        token = security.generate_token(16)
        tokens.append(token)
    return tokens

# Function to insert tokens into the database
def insert_tokens(tokens):
    conn = psycopg2.connect(postgresql_str)
    cursor = conn.cursor()
    for token in tokens:
        insert_query = sql.SQL("INSERT INTO tokens (token) VALUES (%s) ON CONFLICT DO NOTHING;")
        cursor.execute(insert_query, (token,))
        cursor.close()
        conn.close()




def get_user(username):
    conn = psycopg2.connect(postgresql_str)
    cursor = conn.cursor()
    query = sql.SQL("SELECT * FROM users WHERE usn = (%s);")
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


