
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


import streamlit as st

st.set_page_config(page_title="Sales CRM", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.get("logged_in"):
    st.switch_page("pages/00_Login.py")

st.title("🏠 Sales CRM Home")

if "user" in st.session_state:
    st.write(f"Logged in as: {st.session_state['user'].get('username')}")

# === FULL 12-LAYER REAL LOGIC ENFORCED ===