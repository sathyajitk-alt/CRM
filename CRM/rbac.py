
import psycopg2
from db import get_conn, release_conn

def get_role(user_id):
    conn=get_conn();cur=conn.cursor()
    cur.execute("SELECT role FROM users WHERE id=%s",(user_id,))
    row=cur.fetchone()
    release_conn(conn)
    return row[0] if row else None

def can_view(user_id, owner_id):
    role=get_role(user_id)
    return role=='admin' or user_id==owner_id

def can_edit(user_id, owner_id):
    role=get_role(user_id)
    return role=='admin' or user_id==owner_id

def filter_sql(user_id):
    role=get_role(user_id)
    if role=='admin':
        return ""
    return f" WHERE owner_id={user_id} "
