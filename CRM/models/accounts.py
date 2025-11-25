
from db import get_conn, release_conn

def list_accounts(user_id, sql_filter):
    conn=get_conn();cur=conn.cursor()
    cur.execute("SELECT id,name,owner_id FROM accounts"+sql_filter)
    rows=cur.fetchall()
    release_conn(conn)
    return rows

def create_account(name, owner_id):
    conn=get_conn();cur=conn.cursor()
    cur.execute("INSERT INTO accounts(name,owner_id) VALUES(%s,%s)",(name,owner_id))
    conn.commit()
    release_conn(conn)
