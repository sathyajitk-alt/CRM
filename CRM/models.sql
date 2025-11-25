-- Full relational schema with opportunities

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    cin TEXT,
    industry TEXT,
    employees TEXT,
    revenue_lakhs TEXT,
    website TEXT,
    address TEXT,
    location TEXT,
    state TEXT,
    pin TEXT,
    lob TEXT,
    premium TEXT,
    dor TEXT,
    channel TEXT,
    insurer TEXT,
    comments TEXT,
    email_pattern TEXT,
    linkedin TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    name TEXT,
    designation TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    linkedin TEXT
);

CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    lob TEXT,
    premium TEXT,
    dor TEXT,
    channel TEXT,
    insurer TEXT,
    comments TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
