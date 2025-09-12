CREATE ROLE woodford_dev WITH NOLOGIN CREATEDB;

CREATE DATABASE daredevil_dev WITH OWNER = woodford_dev;
CREATE DATABASE daredevil_test WITH OWNER = woodford_dev;

