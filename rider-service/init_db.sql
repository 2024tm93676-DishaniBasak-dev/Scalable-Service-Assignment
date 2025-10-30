
-- Rider Microservice Database Initialization Script 
-- This script:
--  Creates the `riders_db` database and tables.
--  Imports rider data from a CSV file (rhfd_riders.csv).
--  Creates the logs table for request logs.

-- Create the database (if not exists)
CREATE DATABASE IF NOT EXISTS riders_db;

-- USE riders_db;    -- No USE statement needed — SQLAlchemy connects directly to riders_db.

-- Table: riders
CREATE TABLE IF NOT EXISTS riders (
  rider_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(200) NOT NULL UNIQUE,
  phone VARCHAR(50),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table: logs_riders
CREATE TABLE IF NOT EXISTS logs_riders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  level VARCHAR(20),
  message TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- CSV import step removed (handled by init_db.py)

-- Import CSV Data into `riders` Table
-- LOAD DATA LOCAL INFILE '/Users/dishanibasak/rider_python_flask/rhfd_riders.csv' -- change the location as per the csv file location
-- INTO TABLE riders
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 LINES
-- (name, email, phone);


-- Verify Data
-- SELECT COUNT(*) FROM riders;
-- SELECT * FROM riders LIMIT 5;
-- SELECT * FROM logs_riders;
