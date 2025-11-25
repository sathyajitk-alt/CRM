
from db import get_conn, release_conn

def list_opps(account_id):
    conn=get_conn();cur=conn.cursor()
    cur.execute("SELECT id,name,amount,stage FROM opportunities WHERE account_id=%s",(account_id,))
    rows=cur.fetchall()
    release_conn(conn)
    return rows

def create_opp(name,amount,stage,account_id):
    conn=get_conn();cur=conn.cursor()
    cur.execute("INSERT INTO opportunities(name,amount,stage,account_id) VALUES(%s,%s,%s,%s)",
                (name,amount,stage,account_id))
    conn.commit()
    release_conn(conn)
