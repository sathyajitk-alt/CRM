
import psycopg2

DB={'host':'localhost','dbname':'salescrm','user':'postgres','password':'password'}

def get_conn():
    return psycopg2.connect(**DB)

def release_conn(conn):
    conn.close()
