-- ====================================================================
-- Agricultural Crop Production Analysis System
-- Relational Database Schema DDL (MySQL 8.0+)
-- ====================================================================

CREATE DATABASE IF NOT EXISTS crop_analysis_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE crop_analysis_db;

-- --------------------------------------------------------------------
-- Table 1: regions
-- Stores geographical location and agro-climatic zoning
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS regions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    state VARCHAR(100) NOT NULL,
    climate_zone VARCHAR(100) DEFAULT 'Subtropical',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_region_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------------------
-- Table 2: crops
-- Stores crop taxonomy and standard production measurement units
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS crops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL DEFAULT 'Cereal',
    default_unit VARCHAR(50) NOT NULL DEFAULT 'Metric Tonnes',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_crop_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------------------
-- Table 3: crop_records
-- Fact table for annual agricultural observation records
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS crop_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crop_id INT NOT NULL,
    region_id INT NOT NULL,
    year INT NOT NULL,
    area_cultivated DOUBLE NOT NULL,
    area_unit VARCHAR(30) NOT NULL DEFAULT 'Hectares',
    production_quantity DOUBLE NOT NULL,
    production_unit VARCHAR(30) NOT NULL DEFAULT 'Metric Tonnes',
    annual_rainfall DOUBLE NULL,
    notes VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints with cascading deletes
    CONSTRAINT fk_record_crop
        FOREIGN KEY (crop_id) REFERENCES crops(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
        
    CONSTRAINT fk_record_region
        FOREIGN KEY (region_id) REFERENCES regions(id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    -- Business rule: Unique crop-region-year combination
    CONSTRAINT uq_crop_region_year
        UNIQUE (crop_id, region_id, year),

    -- Query optimization indexes
    INDEX idx_records_year (year),
    INDEX idx_records_crop (crop_id),
    INDEX idx_records_region (region_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
