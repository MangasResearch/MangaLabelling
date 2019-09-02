DROP TABLE IF EXISTS dataset;

CREATE TABLE dataset(
  id SERIAL PRIMARY KEY,
  ref text NOT NULL,
  label integer,
  busy boolean NOT NULL,
  marked boolean NOT NULL
);
