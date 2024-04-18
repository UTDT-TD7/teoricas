CREATE TABLE nyse (
    ticker CHAR(10),
    close_value DECIMAL(10, 2),
    date DATE,
    PRIMARY KEY (ticker, date)
);
