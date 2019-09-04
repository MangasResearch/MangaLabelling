DROP TABLE IF EXISTS dataset;

CREATE TABLE dataset(
  id SERIAL PRIMARY KEY,
  ref text NOT NULL,
  label text,
  busy boolean NOT NULL,
  marked boolean NOT NULL
);
