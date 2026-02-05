-- PostgreSQL Initialization Script for Finance Tracker
-- This script runs automatically when the container is first created

-- Create extensions (optional but useful)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search

-- Set timezone
SET timezone = 'Asia/Kolkata';

-- Create additional schemas if needed (optional)
-- CREATE SCHEMA IF NOT EXISTS finance;

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'Finance Tracker database initialized successfully!';
END $$;
