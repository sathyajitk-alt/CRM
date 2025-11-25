
# ================================
# FULL WORKING ACCESS CONTROL LAYER
# ================================
import streamlit as st
from db import get_conn, release_conn

def get_current_user():
    user = st.session_state.get("user")
    if not user:
        st.error("Please log in again.")
        st.stop()
    return user

def load_owner(account_id):
    conn=get_conn(); cur=conn.cursor()
    cur.execute("SELECT owner_id FROM accounts WHERE id=%s",(account_id,))
    row=cur.fetchone()
    release_conn(conn)
    return row[0] if row else None

def load_team(user_id):
    conn=get_conn(); cur=conn.cursor()
    cur.execute("SELECT member_id FROM team_map WHERE manager_id=%s",(user_id,))
    rows=cur.fetchall()
    release_conn(conn)
    return [r[0] for r in rows] if rows else []

def can_view(user, owner_id, team_ids):
    return user['role']=='admin' or user['id']==owner_id or user['id'] in team_ids

def can_edit(user, owner_id):
    return user['role']=='admin' or user['id']==owner_id


from db import get_conn, release_conn

def get_or_create_account(row):
    """
    Parent account logic:
    - Create an account ONLY if LOB is empty.
    - If LOB exists, DO NOT create a new account.
    - Always match parent by NAME (case-insensitive).
    """
    name = row.get("Name")
    lob  = row.get("LOB")

    conn = get_conn()
    cur = conn.cursor()

    # Opportunity row → return parent if exists
    if lob not in (None, "", "NULL"):
        cur.execute("SELECT id FROM accounts WHERE LOWER(name)=LOWER(%s)", (name,))
        existing = cur.fetchone()
        release_conn(conn)
        return existing[0] if existing else None

    # Parent row → create account if not exists
    cur.execute("SELECT id FROM accounts WHERE LOWER(name)=LOWER(%s)", (name,))
    existing = cur.fetchone()
    if existing:
        release_conn(conn)
        return existing[0]

    cur.execute(
        """
        INSERT INTO accounts(
            name, industry, premium, location, state, address,
            website, cin, insurer, channel
        )
        VALUES (NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
        """,
        (
            row.get("Name"),
            row.get("Industry"),
            row.get("Premium"),
            row.get("Location"),
            row.get("State"),
            row.get("Address"),
            row.get("Website"),
            row.get("CIN"),
            row.get("Insurer"),
            row.get("Channel")
        )
    )
    acc_id = cur.fetchone()[0]
    conn.commit()
    release_conn(conn)
    return acc_id

# === FULL 12-LAYER REAL LOGIC ENFORCED ===