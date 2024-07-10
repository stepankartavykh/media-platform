#!/bin/bash

echo "start setting up database storage"
psql postgresql://admin:password@localhost:5500/postgres <<-EOSQL

CREATE DATABASE storage;
\c storage
CREATE SCHEMA articles;

EOSQL

echo "end of creating database storage structure"