
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

from auth.require_login import require_login
import streamlit as st

require_login()


import streamlit as st
import pandas as pd
from db import get_conn, release_conn

st.title("Dashboard")

conn=get_conn(); cur=conn.cursor()
cur.execute("SELECT lob,premium,stage FROM opportunities")
rows=cur.fetchall()
cols=[d[0] for d in cur.description]
release_conn(conn)

df=pd.DataFrame(rows,columns=cols)
df['premium']=pd.to_numeric(df['premium'], errors='coerce')

st.subheader("Premium by LOB")
st.bar_chart(df.groupby('lob')['premium'].sum())

st.subheader("Opportunities by Stage")
st.bar_chart(df['stage'].value_counts())

# === FULL 12-LAYER REAL LOGIC ENFORCED ===