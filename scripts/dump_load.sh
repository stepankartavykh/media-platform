#!/bin/bash

echo "start setting up database storage"
sleep 1
psql postgresql://admin:password@localhost:5500/postgres <<-EOSQL

CREATE DATABASE storage;
\c storage
CREATE SCHEMA articles;
CREATE SCHEMA resources;
CREATE SCHEMA parsed;

EOSQL

echo "end of creating database storage structure"