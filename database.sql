CREATE DATABASE central_116_database;

\c central_116_database;

CREATE TABLE snapshots (
  key SERIAL PRIMARY KEY,
  datetime BIGINT NOT NULL,
  snapshot VARCHAR(255) NOT NULL,
  url VARCHAR(255) NOT NULL,
  origin VARCHAR(255) NOT NULL
);