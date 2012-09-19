SET CLIENT_ENCODING = 'UTF8';
SET CHECK_FUNCTION_BODIES = FALSE;
SET CLIENT_MIN_MESSAGES = WARNING;

CREATE TABLE topic (
    topic_id          TEXT                     PRIMARY KEY,
    group_id          TEXT                     NOT NULL,
    site_id           TEXT                     NOT NULL,
    original_subject  TEXT                     NOT NULL,
    first_post_id     TEXT                     NOT NULL REFERENCES post (post_id),
    last_post_id      TEXT                     NOT NULL REFERENCES post (post_id),
    last_post_date    TIMESTAMP WITH TIME ZONE NOT NULL,
    num_posts         INTEGER                  NOT NULL CHECK (num_posts > 0),
    hidden            TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    sticky            TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    -- A PostgreSQL dependency is created by the TEXT array and tsvector.
    keywords          TEXT[]                   DEFAULT NULL,
    fts_vectors       tsvector
);  

-- Installs up to and including GS 12.05 will need to update the topic
-- table:
-- ALTER TABLE topic ADD COLUMN keywords TEXT[] DEFAULT NULL;
-- ALTER TABLE topic ADD COLUMN fts_vectors tsvector;
-- DROP TABLE topic_word_count;
-- DROP TABLE word_count;

CREATE INDEX GROUP_ID_SITE_ID_IDX ON topic USING BTREE (group_id, site_id);
-- ALTER TABLE topic ADD column hidden TIMESTAMP WITH TIME ZONE;
CREATE INDEX topic_fts_vectors ON topic USING gin(fts_vectors);

-- See 03-keywords.sql in this directory for the trigger that updates the
-- fts_vectors and keywords columns.
