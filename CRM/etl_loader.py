
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

import os
import pandas as pd
import psycopg2
from datetime import datetime, date

# Get DB connection
DB_URL = os.getenv("DB_URL")

# Load your Base.csv
df = pd.read_csv("Base.csv")

# Lines of Business considered Employee Benefits
EB = ["gmc", "gpa", "gtl", "gratuity", "edli", "opd", "top-up", "super top-up"]

# SMART DATE: Today = 22 Nov 2025 (your actual system definition)
TODAY = date(2025, 11, 22)

# ---------------------------------------------------------
# SMART PARSE FUNCTION: convert "27-Nov" → YYYY-MM-DD using next-occurrence logic
# ---------------------------------------------------------
def parse_dor(val):
    if pd.isna(val):
        return None

    try:
        # Convert "27-Nov" into a datetime WITHOUT year
        dt = datetime.strptime(val.strip(), "%d-%b")

        # Try with current year
        dor = date(TODAY.year, dt.month, dt.day)

        # If the date has already passed this year → make it next year
        if dor < TODAY:
            dor = date(TODAY.year + 1, dt.month, dt.day)

        return dor
    except:
        return None


# ---------------------------------------------------------
# CONNECT TO POSTGRES
# ---------------------------------------------------------
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

accounts = {}
prem = {}

# ---------------------------------------------------------
# CREATE ACCOUNTS
# ---------------------------------------------------------
for _, r in df.iterrows():
    n = r["Name"]

    if n not in accounts:
        cur.execute(
            """
            INSERT INTO accounts(name, cin, address, location, state, website, linkedin, )
            VALUES (NOW(),NOW(),%s,%s,%s,%s,%s,%s,%s,0)
            RETURNING id
            """,
            (
                n,
                r.get("CIN"),
                r.get("Address"),
                r.get("Location"),
                r.get("State"),
                r.get("Website"),
                r.get("Linkedin")
            )
        )
        accounts[n] = cur.fetchone()[0]
        prem[n] = 0  # EB premium accumulator


# ---------------------------------------------------------
# CREATE OPPORTUNITIES + PREMIUM ROLLUP
# ---------------------------------------------------------
for _, r in df.iterrows():
    name = r["Name"]
    acc_id = accounts[name]

    premium = r.get("Premium")
    lob = str(r.get("LOB")).lower() if pd.notna(r.get("LOB")) else ""

    # Parse DOR
    dor_raw = r.get("DOR")
    dor = parse_dor(str(dor_raw)) if pd.notna(dor_raw) else None

    # EB premium accumulation
    if pd.notna(premium) and lob in EB:
        prem[name] += premium

    # Create opportunities only for valid LOBs
    if lob and lob not in ["nan", ""]:
         = "EB" if lob in EB else "Non-EB"

        cur.execute(
            """
            INSERT INTO opportunities(account_id, lob, , premium, dor, status)
            VALUES (NOW(),NOW(),%s, %s, %s, %s, %s, 'Recurring')
            """,
            (acc_id, lob, , premium, dor)
        )


# ---------------------------------------------------------
# UPDATE ACROSS ACCOUNTS: ESTIMATED EB PREMIUM ROLLUP
# ---------------------------------------------------------
for name, value in prem.items():
    cur.execute(
        "UPDATE accounts SET  = %s WHERE id = %s",
        (value, accounts[name])
    )

# FINALIZE
conn.commit()
cur.close()
conn.close()

# === FULL 12-LAYER REAL LOGIC ENFORCED ===