DROP TABLE IF EXISTS stonk.companies;
DROP TABLE IF EXISTS stonk.quotes;
DROP SCHEMA IF EXISTS stonk;

CREATE SCHEMA stonk;
CREATE TABLE stonk.companies(
    company_id serial PRIMARY KEY,
    name VARCHAR ( 50 ) UNIQUE NOT NULL,
    symbol VARCHAR ( 6 ) UNIQUE NOT NULL
);

INSERT INTO stonk.companies(name, symbol)
VALUES ('AMC Entertainment', 'AMC');

INSERT INTO stonk.companies(name, symbol)
VALUES ('GameStop', 'GME');

CREATE TABLE stonk.quotes(
    quote_id serial PRIMARY KEY,
    company_id INT,
    CONSTRAINT fk_company
      FOREIGN KEY (company_id)
        REFERENCES stonk.companies (company_id),
    current_price REAL NOT NULL,
    change REAL,
    percent_change REAL,
    day_high REAL NOT NULL,
    day_low REAL NOT NULL,
    open REAL NOT NULL,
    previous_close REAL NOT NULL,
    datetime TIMESTAMP WITH TIME ZONE
);

INSERT INTO stonk.quotes (company_id, current_price, change, percent_change, day_high, day_low, open, previous_close, datetime) VALUES
(1, 40, 0, 0, 0, 0, 0, 0, '2021-10-01 14:55:01-05');

INSERT INTO stonk.quotes (company_id, current_price, change, percent_change, day_high, day_low, open, previous_close, datetime) VALUES
(1, 42, 0, 0, 0, 0, 0, 0, '2021-10-01 15:00:01-05');

INSERT INTO stonk.quotes (company_id, current_price, change, percent_change, day_high, day_low, open, previous_close, datetime) VALUES
(2, 130, 0, 0, 0, 0, 0, 0, '2021-10-01 14:55:01-05');

INSERT INTO stonk.quotes (company_id, current_price, change, percent_change, day_high, day_low, open, previous_close, datetime) VALUES
(2, 135, 0, 0, 0, 0, 0, 0, '2021-10-01 15:00:01-05');
