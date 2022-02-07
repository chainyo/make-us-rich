/* Add extension for password */
CREATE EXTENSION pgcrypto;

/* Create table for users */
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
);

/* Create table for roles */
CREATE TABLE IF NOT EXISTS roles (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

/* Create table for user's roles */
CREATE TABLE IF NOT EXISTS user_roles (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  role_id INTEGER NOT NULL,
  CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT role_id_fk FOREIGN KEY (role_id) REFERENCES roles (id)
);

/* Insert roles */
INSERT INTO roles (name) VALUES ('admin');
INSERT INTO roles (name) VALUES ('member');
