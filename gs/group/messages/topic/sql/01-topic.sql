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
    sticky            TIMESTAMP WITH TIME ZONE DEFAULT NULL
);  
CREATE INDEX GROUP_ID_SITE_ID_IDX ON topic USING BTREE (group_id, site_id);
-- ALTER TABLE topic ADD column hidden TIMESTAMP WITH TIME ZONE;

-- A faux full-text system
CREATE TABLE topic_word_count (
    topic_id          TEXT                     NOT NULL REFERENCES topic (topic_id),
    word              TEXT                     NOT NULL,
    count             INTEGER                  NOT NULL CHECK (count > 0)
);
CREATE UNIQUE INDEX TOPIC_WORD_PKEY ON topic_word_count USING BTREE (topic_id, word);

CREATE TABLE word_count (
    word text NOT NULL,
    count integer NOT NULL
);
CREATE UNIQUE INDEX WORD_COUNT_PKEY ON word_count USING BTREE (word);

