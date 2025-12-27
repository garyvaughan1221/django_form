sql

CREATE TABLE state_names (
  `StateCode` VARCHAR(2) NOT NULL,
  StateName VARCHAR(7) NOT NULL,
  PRIMARY KEY (`StateCode`),
  UNIQUE KEY stateNames_StateCode_key (`StateCode`)
);

CREATE TABLE county_names (
  `StateCode` VARCHAR(2) NOT NULL,
  CountyName VARCHAR(14) NOT NULL,
  FIPS INT NOT NULL,
  PRIMARY KEY (FIPS),
  UNIQUE KEY county_names_FIPS_key (FIPS),
  CONSTRAINT county_names_StateCode_fkey FOREIGN KEY (`StateCode`) REFERENCES state_names (`StateCode`)
);
CREATE INDEX IF NOT EXISTS statecode_countynames ON county_names (`StateCode`);
CREATE INDEX IF NOT EXISTS fips_countynames ON county_names (FIPS);

CREATE TABLE church_orgs (
  GroupName VARCHAR(20) NOT NULL,
  `GroupCode` VARCHAR(3) NOT NULL,
  PRIMARY KEY (`GroupCode`),
  UNIQUE KEY church_orgs_GroupCode_key (`GroupCode`),
  UNIQUE KEY church_orgs_GroupName_key (GroupName)
);
CREATE INDEX IF NOT EXISTS groupcode_churchorgs ON church_orgs (`GroupCode`);



CREATE TABLE national (
  id INT PRIMARY KEY AUTO_INCREMENT,
  `GroupCode` VARCHAR(3) NOT NULL,
  Congregations INT NULL,
  Adherents INT NULL,
  Adherents_percent_of_Total_Adherents FLOAT NULL,
  Adherents_percent_of_Population FLOAT NULL
);

CREATE TABLE by_state (
  id BIGINT NOT NULL AUTO_INCREMENT,
  `StateCode` VARCHAR(2) NOT NULL,
  `GroupCode` VARCHAR(3) NOT NULL,
  Congregations INT NULL,
  Adherents INT NULL,
  Adherents_percent_of_Total_Adherents FLOAT NULL,
  Adherents_percent_of_Population FLOAT NULL,
  PRIMARY KEY (id),
  CONSTRAINT by_state_StateCode_fkey FOREIGN KEY (`StateCode`) REFERENCES state_names (`StateCode`)
);
CREATE INDEX IF NOT EXISTS statecode_bystate ON by_state (`StateCode`);

CREATE TABLE by_county (
  id BIGINT NOT NULL AUTO_INCREMENT,
  `StateCode` VARCHAR(2) NOT NULL,
  FIPS INT NOT NULL,
  `GroupCode` VARCHAR(3) NOT NULL,
  Congregations INT NULL,
  Adherents INT NULL,
  Adherents_percent_of_Total_Adherents FLOAT NULL,
  Adherents_percent_of_Population FLOAT NULL,
  PRIMARY KEY (id),
  CONSTRAINT by_county_GroupCode_fkey FOREIGN KEY (`GroupCode`) REFERENCES church_orgs (`GroupCode`),
  CONSTRAINT by_county_StateCode_fkey FOREIGN KEY (`StateCode`) REFERENCES state_names (`StateCode`)
);
CREATE INDEX IF NOT EXISTS fips_bycounty ON by_county (FIPS);
CREATE INDEX IF NOT EXISTS statecode_bycounty ON by_county (`StateCode`);

