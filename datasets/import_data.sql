LOAD DATA LOCAL INFILE '/home/garuwun/django_form/datasets/state_names_rows.csv'
INTO TABLE state_names
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA LOCAL INFILE '/home/garuwun/django_form/datasets/county_names_rows.csv'
INTO TABLE county_names
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA LOCAL INFILE '/home/garuwun/django_form/datasets/church_orgs_rows.csv'
INTO TABLE church_orgs
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/home/garuwun/django_form/datasets/national_rows.csv'
INTO TABLE national
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/home/garuwun/django_form/datasets/by_state_rows.csv'
INTO TABLE by_state
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/home/garuwun/django_form/datasets/by_county_rows.csv'
INTO TABLE by_county
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;