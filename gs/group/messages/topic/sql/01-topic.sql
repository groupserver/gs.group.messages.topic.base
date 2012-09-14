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
    keywords          TEXT                     DEFAULT NULL,
    fts_vectors       tsvector -- PostgreSQL dependency
);  

-- Installs up to and including GS 12.05 will need to update the topic
-- table:
-- ALTER TABLE topic ADD COLUMN keywords TEXT DEFAULT NULL;
-- ALTER TABLE topic ADD COLUMN fts_vectors tsvector;
-- DROP TABLE topic_word_count;
-- DROP TABLE word_count;

CREATE INDEX GROUP_ID_SITE_ID_IDX ON topic USING BTREE (group_id, site_id);
-- ALTER TABLE topic ADD column hidden TIMESTAMP WITH TIME ZONE;
CREATE INDEX topic_fts_vectors ON topic USING gin(fts_vectors);

-- Installs up to and including GS 12.05 will need to populate the
--   full-text search column of the topic table.
-- CREATE OR REPLACE FUNCTION topic_fts_vectors_populate () RETURNS void AS $$
-- DECLARE
--    trecord RECORD;
--  BEGIN
--    FOR trecord IN SELECT * FROM topic WHERE tsv IS NULL LOOP
--      UPDATE topic 
--        SET tsv=to_tsvector('english', ss.agg_body) 
--        FROM (SELECT string_agg(body, '') AS agg_body
--                FROM post, topic 
--                WHERE post.topic_id = trecord.topic_id
--                      AND post.topic_id = topic.topic_id
--                      AND topic.fts_vectors IS NULL) AS ss 
--        WHERE topic_id=trecord.topic_id;
--    END LOOP;
--  END;
-- $$ LANGUAGE 'plpgsql';

-- The topic fts_vectors column contains the full-text retrieval
--   information for all the posts in the topic. It is updated after a
--   *post* has been added to the database. In effect it concatenates all
--   the bodies together (string_agg(post.body, ' ')) and turns them into a
--   text-search vector (to_tsvector).
CREATE OR REPLACE FUNCTION topic_fts_vectors_update ()
  RETURNS TRIGGER
  AS $$
    BEGIN
      UPDATE topic 
        SET topic.fts_vectors = to_tsvector('english', ss.agg_body) 
        FROM (SELECT string_agg(post.body, ' ') AS agg_body
              FROM post
              WHERE post.topic_id = NEW.topic_id) AS ss 
        WHERE topic.topic_id = NEW.topic_id;
      RETURN NULL;
    END;  
  $$ LANGUAGE plpgsql;
CREATE TRIGGER topic_fts_vectors_update_trigger 
  AFTER INSERT OR UPDATE ON post -- Yes, AFTER; yes, post.
  EXECUTE PROCEDURE topic_fts_vectors_update ();
