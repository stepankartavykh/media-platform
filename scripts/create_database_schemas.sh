#!/bin/bash

echo "LOG: Start creating database storage schemas..."
psql postgresql://admin:password@localhost:5432/postgres <<-EOSQL

CREATE DATABASE storage;
\c storage

CREATE SCHEMA articles;
CREATE SCHEMA resources;
CREATE SCHEMA parsed;
CREATE SCHEMA actual_content;
CREATE SCHEMA events;
CREATE SCHEMA raw;

EOSQL

echo "LOG: Schemas are created."