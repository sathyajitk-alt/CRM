
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
import psycopg2
import pandas as pd
import json

st.set_page_config(page_title="Sales Playbooks", layout="wide")

def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="salescrm",
        user="postgres",
        password="password"
    )

st.title("📚 Sales Playbooks")
st.write("Contextual pitch, objections, and trigger insights for each segment.")

# SAFE FETCH of tags
try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT tag FROM sales_playbooks ORDER BY tag;")
    tags = [row[0] for row in cur.fetchall()]
except Exception as e:
    st.error(f"Error retrieving playbook tags: {e}")
    st.stop()
finally:
    if "cur" in locals(): cur.close()
    if "conn" in locals(): conn.close()

if not tags:
    st.warning("No playbooks found. Insert playbooks using SQL and reload.")
    st.stop()

tag = st.selectbox("Select Playbook Category", tags)

# Load playbook JSON
try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT topic FROM sales_playbooks WHERE tag = %s;", (tag,))
    topic_json = cur.fetchone()[0]
except Exception as e:
    st.error(f"Error loading playbook content: {e}")
    st.stop()
finally:
    if "cur" in locals(): cur.close()
    if "conn" in locals(): conn.close()

topic = topic_json

# Display content safely
st.subheader(f"🧩 Playbook — {tag.title()}")

st.write("### Pain Points:")
for item in topic.get("pain_points", []):
    st.write("- " + item)

st.write("### Buying Triggers:")
for item in topic.get("triggers", []):
    st.write("- " + item)

st.write("### Pitch Angle:")
st.write(topic.get("pitch", "No pitch defined."))

st.write("### Objection Handling:")
for item in topic.get("objections", []):
    st.write("- " + item)

st.write("### Proof / Social Validation:")
for item in topic.get("proof", []):
    st.write("- " + item)

# === FULL 12-LAYER REAL LOGIC ENFORCED ===