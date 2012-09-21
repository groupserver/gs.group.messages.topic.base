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

-- ALTER TABLE topic ADD column hidden TIMESTAMP WITH TIME ZONE;

-- Installs up to and including GS 12.05 will need to update the topic
-- table:
-- ALTER TABLE topic ADD COLUMN keywords TEXT[] DEFAULT NULL;
-- ALTER TABLE topic ADD COLUMN fts_vectors tsvector;
-- DROP TABLE topic_word_count;
-- DROP TABLE word_count;

CREATE INDEX GROUP_ID_SITE_ID_IDX ON topic USING BTREE (group_id, site_id);
CREATE INDEX topic_fts_vectors ON topic USING gin(fts_vectors);


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
    SELECT COALESCE(original_subject, '') INTO subject
      FROM topic WHERE topic.topic_id = topic_body.topic_id;
    retval := left(subject || ' ' || topic_text, 1048575); -- Max for a vector
    RETURN retval;
  END;
$$ LANGUAGE 'plpgsql';


-- The trigger for updating the full-text retrieval information, and the
-- keywords, in a topic. The topic fts_vectors column contains the
-- full-text retrieval information for all the posts in the topic. It is
-- updated after a *post* has been added to the database.
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
