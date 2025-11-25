
from db import get_conn, release_conn

def list_contacts(account_id):
    conn=get_conn();cur=conn.cursor()
    cur.execute("SELECT id,name,email,phone FROM contacts WHERE account_id=%s",(account_id,))
    rows=cur.fetchall()
    release_conn(conn)
    return rows

def create_contact(name,email,phone,account_id):
    conn=get_conn();cur=conn.cursor()
    cur.execute("INSERT INTO contacts(name,email,phone,account_id) VALUES(%s,%s,%s,%s)",
                (name,email,phone,account_id))
    conn.commit()
    release_conn(conn)
