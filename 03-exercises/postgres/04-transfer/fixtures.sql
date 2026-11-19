CREATE TABLE accounts(id bigint PRIMARY KEY, balance bigint NOT NULL CHECK(balance >= 0));
INSERT INTO accounts VALUES (1,10000),(2,10000),(3,0);
