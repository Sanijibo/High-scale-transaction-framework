-- Enable PostGIS for geospatial tracking
CREATE EXTENSION IF NOT EXISTS postgis;

-- Parent table partitioned by month
CREATE TABLE transactions (
    id UUID NOT NULL,
    merchant_id UUID NOT NULL,
    amount DECIMAL(18, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'NGN',
    status VARCHAR(20) NOT NULL,
    location GEOGRAPHY(POINT), 
    metadata JSONB, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Specialized indexing for sub-second queries
CREATE INDEX idx_transactions_location ON transactions USING GIST (location);
CREATE INDEX idx_transactions_metadata ON transactions USING GIN (metadata);

-- Create initial partition for the current month
CREATE TABLE transactions_2025_12 PARTITION OF transactions
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');
