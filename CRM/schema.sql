
CREATE TABLE accounts (
 id SERIAL PRIMARY KEY,
 name TEXT,
 cin TEXT,
 address TEXT,
 location TEXT,
 state TEXT,
 website TEXT,
 linkedin TEXT,
 estimated_total_premium NUMERIC,
 created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE contacts (
 id SERIAL PRIMARY KEY,
 account_id INT REFERENCES accounts(id),
 name TEXT,
 email TEXT,
 phone TEXT,
 designation TEXT,
 contact_type TEXT,
 created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE opportunities (
 id SERIAL PRIMARY KEY,
 account_id INT REFERENCES accounts(id),
 lob TEXT,
 policy_type TEXT,
 premium NUMERIC,
 dor DATE,
 status TEXT,
 created_at TIMESTAMP DEFAULT NOW()
);
