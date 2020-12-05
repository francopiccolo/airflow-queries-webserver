DROP TABLE IF EXISTS events_stg;
CREATE TABLE IF NOT EXISTS events_stg (
    event               VARCHAR(50),
    time                TIMESTAMP,
    unique_visitor_id   VARCHAR(200),
    ha_user_id          VARCHAR(50),
    browser             VARCHAR(50),
    os                  VARCHAR(50),
    country_code        VARCHAR(50)
);

DROP TABLE IF EXISTS events;
CREATE TABLE IF NOT EXISTS events (
    event               VARCHAR(50),
    time                TIMESTAMP,
    unique_visitor_id   VARCHAR(200),
    ha_user_id          VARCHAR(50),
    browser             VARCHAR(50),
    os                  VARCHAR(50),
    country_code        VARCHAR(50)
);