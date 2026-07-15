-- =============================================================
-- AI-First Healthcare CRM — Database Schema
-- Database: PostgreSQL 15+
-- =============================================================

-- Enable UUID extension for generating unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================
-- Table: hcp_profiles
-- Stores Healthcare Professional (doctor) profiles
-- =============================================================
CREATE TABLE IF NOT EXISTS hcp_profiles (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(255) NOT NULL,
    hospital        VARCHAR(255),
    specialization  VARCHAR(150),
    phone           VARCHAR(20),
    email           VARCHAR(255),
    preferred_contact VARCHAR(50) DEFAULT 'email'
                    CHECK (preferred_contact IN ('email', 'phone', 'in-person', 'video-call')),
    notes           TEXT,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for fast lookups by name
CREATE INDEX idx_hcp_profiles_name ON hcp_profiles (LOWER(name));
CREATE INDEX idx_hcp_profiles_specialization ON hcp_profiles (specialization);

-- =============================================================
-- Table: hcp_interactions
-- Logs every interaction between a sales rep and a doctor
-- =============================================================
CREATE TABLE IF NOT EXISTS hcp_interactions (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hcp_id              UUID NOT NULL REFERENCES hcp_profiles(id) ON DELETE CASCADE,
    interaction_type    VARCHAR(50) NOT NULL
                        CHECK (interaction_type IN ('in-person', 'phone', 'email', 'video-call', 'conference')),
    date                DATE NOT NULL,
    time                TIME,
    attendees           TEXT[],
    topics_discussed    TEXT[],
    sentiment           VARCHAR(20)
                        CHECK (sentiment IN ('positive', 'neutral', 'negative', 'mixed')),
    outcomes            TEXT,
    follow_up_actions   TEXT[],
    summary             TEXT,
    ai_generated        BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for common query patterns
CREATE INDEX idx_interactions_hcp_id ON hcp_interactions (hcp_id);
CREATE INDEX idx_interactions_date ON hcp_interactions (date DESC);
CREATE INDEX idx_interactions_type ON hcp_interactions (interaction_type);
CREATE INDEX idx_interactions_sentiment ON hcp_interactions (sentiment);

-- =============================================================
-- Table: materials
-- Marketing and educational materials shared with HCPs
-- =============================================================
CREATE TABLE IF NOT EXISTS materials (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(255) NOT NULL,
    type        VARCHAR(100) NOT NULL
                CHECK (type IN ('brochure', 'clinical-study', 'product-sheet', 'presentation', 'whitepaper', 'video', 'other')),
    description TEXT,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_materials_type ON materials (type);

-- =============================================================
-- Table: samples
-- Product samples distributed to HCPs
-- =============================================================
CREATE TABLE IF NOT EXISTS samples (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        VARCHAR(255) NOT NULL,
    product     VARCHAR(255) NOT NULL,
    quantity    INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_samples_product ON samples (product);

-- =============================================================
-- Table: interaction_materials (Junction)
-- Links interactions to materials shared during that interaction
-- =============================================================
CREATE TABLE IF NOT EXISTS interaction_materials (
    interaction_id  UUID NOT NULL REFERENCES hcp_interactions(id) ON DELETE CASCADE,
    material_id     UUID NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    PRIMARY KEY (interaction_id, material_id)
);

-- =============================================================
-- Table: interaction_samples (Junction)
-- Links interactions to samples distributed during that interaction
-- =============================================================
CREATE TABLE IF NOT EXISTS interaction_samples (
    interaction_id  UUID NOT NULL REFERENCES hcp_interactions(id) ON DELETE CASCADE,
    sample_id       UUID NOT NULL REFERENCES samples(id) ON DELETE CASCADE,
    quantity        INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    PRIMARY KEY (interaction_id, sample_id)
);

-- =============================================================
-- Trigger: Auto-update `updated_at` on row modification
-- =============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_hcp_profiles_updated_at
    BEFORE UPDATE ON hcp_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_hcp_interactions_updated_at
    BEFORE UPDATE ON hcp_interactions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
