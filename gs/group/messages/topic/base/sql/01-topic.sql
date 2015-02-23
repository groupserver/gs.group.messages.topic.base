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
    last_post_date    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    num_posts         INTEGER                  NOT NULL CHECK (num_posts > 0),
    hidden            TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    sticky            TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    -- A PostgreSQL dependency is created by the TEXT array and tsvector.
    fts_vectors       tsvector
);  

-- ALTER TABLE topic ADD column hidden TIMESTAMP WITH TIME ZONE;

CREATE INDEX GROUP_ID_SITE_ID_IDX ON topic USING BTREE (group_id, site_id);
-- To make searching faster.
CREATE INDEX topic_fts_vectors ON topic USING gin(fts_vectors);
-- To make the generation of the most-recent topics list faster.
CREATE INDEX topic_last_post_date_idx ON topic (last_post_date DESC);

-- Get the body of all the posts in a topic as a single string
--
-- ARGUMENTS
--
--   topic_id  The identifier for the topic.
--
-- RETURNS
--
--   A single string that is made up from of all bodies of all the posts in
--   the topic. It is limited to 1048575 characters, as that is the maximum
--   length for a vector.
CREATE OR REPLACE FUNCTION topic_body (topic_id TEXT)
  RETURNS TEXT AS $$
  DECLARE
      topic_text TEXT;
      subject TEXT;
      retval TEXT;
  BEGIN
    SELECT string_agg(post.body, ' ') INTO topic_text
      FROM post 
      WHERE post.topic_id = topic_body.topic_id
        AND post.hidden IS NULL;
    SELECT COALESCE(post.subject, '') INTO subject
      FROM post WHERE post.topic_id = topic_body.topic_id LIMIT 1;
    retval := left(subject || ' ' || topic_text, 1048575); -- Max for a vector
    RETURN retval;
  END;
$$ LANGUAGE 'plpgsql';


-- Installs up to and including GS 12.05 will need to update the topic
-- table:
-- ALTER TABLE topic ADD COLUMN fts_vectors tsvector;
-- DROP TABLE topic_word_count;
-- DROP TABLE word_count;
-- 
-- Installs up to and including GS 12.05 will need to populate the
-- full-text retrieval column of the topic table.
-- CREATE OR REPLACE FUNCTION topic_ftr_populate () 
--   RETURNS void AS $$ 
--     DECLARE
--       total_topics REAL;
--       trecord RECORD;
--       topic_vector tsvector;
--       topic_text TEXT;
--       i REAL DEFAULT 0;
--       p REAL;
--     BEGIN
--       SELECT CAST(total_rows AS REAL) INTO total_topics
--         FROM rowcount WHERE table_name = 'topic';
--       FOR trecord IN SELECT * FROM topic WHERE fts_vectors IS NULL LOOP
--         RAISE NOTICE 'Topic %', trecord.topic_id;
--         topic_vector := to_tsvector('english', topic_body(trecord.topic_id));
--         UPDATE topic SET fts_vectors = topic_vector 
--           WHERE topic.topic_id = trecord.topic_id;
--         i := i + 1;
--         p := (i / total_topics) * 100;
--         RAISE NOTICE '  Progress % %%', p;
--       END LOOP;
--     END;
-- $$ LANGUAGE 'plpgsql';


-- The trigger for updating the full-text retrieval information in a topic.
CREATE OR REPLACE FUNCTION topic_fts_update ()
  RETURNS TRIGGER AS $$
    DECLARE
      topic_text TEXT;
    BEGIN
      topic_text := topic_body(NEW.topic_id);
      NEW.fts_vectors := to_tsvector('english', topic_text);
      RETURN NEW;
    END;  
$$ LANGUAGE 'plpgsql';
CREATE TRIGGER topic_update_trigger_01
  BEFORE INSERT OR UPDATE ON topic
  FOR EACH ROW EXECUTE PROCEDURE topic_fts_update ();

