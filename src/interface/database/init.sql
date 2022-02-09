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

/* Create table for API tokens */
CREATE TABLE IF NOT EXISTS api_tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  token TEXT NOT NULL,
  CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users (id)
);

/* Create table for API consumption limit per user */
CREATE TABLE IF NOT EXISTS api_consumption_limit (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  api_limit INTEGER NOT NULL,
  CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users (id)
);

/* Insert roles */
INSERT INTO roles (name) VALUES ('admin');
INSERT INTO roles (name) VALUES ('member');
