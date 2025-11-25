
import psycopg2

def apply_schema_patch():
    sql = """-- FINAL FULL IMPLEMENTATION SCHEMA PATCH
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS owner_id INT;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS owner_id INT;
ALTER TABLE opportunities ADD COLUMN IF NOT EXISTS owner_id INT;

CREATE TABLE IF NOT EXISTS team_map (
    manager_id INT,
    member_id INT
);
"""

    conn = psycopg2.connect(
        host="localhost",
        database="yourdbname",
        user="postgres",
        password="yourpassword"
    )
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Schema patch applied successfully!")

if __name__ == "__main__":
    apply_schema_patch()
