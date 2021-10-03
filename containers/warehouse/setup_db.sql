CREATE SCHEMA stonk;
CREATE TABLE stonk.quotes(
    quote_id serial PRIMARY KEY,
    company_id INT,
    CONSTRAINT fk_company
      FOREIGN KEY (company_id)
        REFERENCES companies (company_id),
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume INT CHECK (volume >= 0),
    datetime TIMESTAMP WITH TIME ZONE
);

CREATE TABLE stonk.companies(
    company_id serial PRIMARY KEY,
    name VARCHAR ( 50 ) UNIQUE NOT NULL,
    symbol VARCHAR ( 6 ) UNIQUE NOT NULL
);

INSERT INTO stonk.companies(name, symbol)
VALUES ('AMC Entertainment', 'AMC');

INSERT INTO stonk.companies(name, symbol)
VALUES ('GameStop', 'GME');
