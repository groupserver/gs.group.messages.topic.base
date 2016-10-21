-- The TF * IDF algorithm, in PL/pgSQL.
--
-- The TF-IDF value for a word = TF * log(IDF). The code below calculates
--   the five top TF-IDF values for a newly updated topic.
SET CLIENT_ENCODING = 'UTF8';
SET CHECK_FUNCTION_BODIES = FALSE;
SET CLIENT_MIN_MESSAGES = WARNING;


-- Calculate the term-frequencies for a topic.
--
-- DESCRIPTION
--
--   The core of the TF-IDF algorithm, the term frequency is
--
--   TF (term frequency) =
--                 Count of the word in the topic
--     _________________________________________________________
--      Count of the most frequently occuring word in the topic
--
--   Sixteen term-frequencies are returned so the rest of the TF-IDF
--   algorithm does not have to deal with all the words that are likely to
--   be dross. However, this does mean that occasionally a great keyword is
--   lost. The speed gain is worth it.
--
-- ARGUMENTS
--
--   topic_id  The identifier of the topic.
--
-- RETURNS
--
--   The stems of the top sixteen words in the topic, as stem-tf pairs.
CREATE OR REPLACE FUNCTION topic_tf (topic_id TEXT)
  RETURNS TABLE (stem TEXT, tf REAL) AS $$
    DECLARE
      ts_stat_inner TEXT;
      most_frequent_word_count REAL;
    BEGIN
      ts_stat_inner := 'SELECT fts_vectors FROM topic WHERE topic_id = ''' || topic_id || '''';
      SELECT CAST(ts.nentry AS REAL) INTO most_frequent_word_count
        FROM ts_stat(ts_stat_inner) as ts
        ORDER BY nentry DESC LIMIT 1;
      RETURN QUERY SELECT cw.word AS stem,
                     CAST(cw.nentry  / most_frequent_word_count AS REAL) AS tf
        FROM (SELECT ts.word, ts.nentry FROM ts_stat(ts_stat_inner) AS ts
                ORDER BY nentry DESC LIMIT 16) as cw; -- Power of 2;
    END;
$$ LANGUAGE plpgsql;


-- TF-IDF: Term Frequency --- Inverse Document Frequency
--
-- DESCRIPTION
--
--   Calculate the five stems with the highest TF-IDF value for a topic.
--
--   TF_IDF = TF * IDF
--   IDF (inverse document frequency) =
--                Total number of topics
--        _________________________________________
--         Count of the topics containing the word
--
--   The IDF value for a word is quite slow to calculate, as all topics
--   have to be searched to get a count. This is why we only do the TF-IDF
--   calculation for the 16 most frequently occurring stems.
--
-- ARGUMENTS
--
--   topic_id  The identifier of the topic.
--
-- RETURNS
--
--   The five stems with the highest TF-IDF values. Returned as a table of
--   stem-value pairs.
CREATE OR REPLACE FUNCTION topic_tf_idf (topic_id TEXT)
  RETURNS TABLE (stem TEXT, tf_idf REAL) AS $$
    DECLARE
      total_topics REAL;
    BEGIN
      SELECT CAST(total_rows AS REAL) INTO total_topics
        FROM rowcount WHERE table_name = 'topic';
      -- The cast of the ttf.stem to tsquery, rather than calling "to_tsquery"
      -- is deliberate.
      RETURN QUERY
        SELECT ttf.stem,
               CAST(ttf.tf *
                    LOG(total_topics /
                        (SELECT COUNT(*) FROM topic
                           WHERE fts_vectors @@ CAST(ttf.stem AS tsquery)))
                    AS REAL)
                  AS tf_idf
        FROM topic_tf(topic_id) as ttf
        ORDER BY tf_idf DESC
        LIMIT 5;
    EXCEPTION
      -- Sometimes the stem that is returned cannot be used (sanely) in a
      -- query, and a syntax error is raised. In that case lets just go
      -- with the TF values. It ain't as good as the TF-IDF values, but it
      -- will do.
      --
      -- Similarly, binary blobs can make it into the database, in which
      -- case we can get division-by-zero errors. Once again, just return
      -- the TF values.
      WHEN syntax_error OR division_by_zero THEN
        RAISE NOTICE 'Caught syntax error';
        RETURN QUERY
          SELECT ttf.stem, ttf.tf AS tf_idf
            FROM topic_tf(topic_id) as ttf
            ORDER BY tf_idf DESC
            LIMIT 5;
    END;
$$ LANGUAGE 'plpgsql';


-- Get all the stem-word pairs for the given topic text
--
-- DESCRIPTION
--
--   The TF-IDF algorithm (above) works on stems, because it gets the topic
--   statistics from the text-search vector (it is faster that
--   way). However, we do not want to present stems to the user, so we
--   generate stem-word pairs so we can map the stems back to "real" words.
--
-- ARGUMENTS
--
--   topic_text  The body of the topic.
--
-- RETURNS
--
--    A table of stem-word pairs. Only one stem is returned, with the
--    shortest version of the word considered canonical.
CREATE OR REPLACE FUNCTION topic_words (topic_text TEXT)
  RETURNS TABLE(stem TEXT, word TEXT) as $$
    BEGIN
      -- The text is processed using the ts_debug function. Let this be a
      --   warning to all: even if you label the function "debug", and put
      --   it in the Debug section of the documentation, evil people such
      --   as myself will still use it for *real* *applications* *outside*
      --   *debugging*. Sorry.
      --   <http://www.postgresql.org/docs/9.1/static/textsearch-debugging.html>
      --
      -- Get one word, and one word only using a combination of DISTINCT ON and
      --   ORDER BY.
      RETURN QUERY SELECT DISTINCT ON (stem) lexemes[1] AS stem, token AS word
                     FROM ts_debug('english', topic_text)
                     WHERE lexemes IS NOT NULL
                       AND lexemes[1] IS NOT NULL
                     ORDER BY stem ASC, word ASC;
    END;
$$ LANGUAGE 'plpgsql';


-- Generate the five words that most characterise the topic
--
-- DESCRIPTION
--
--   The keywords in a topic are words that appear frequently in *this*
--   topic but do not appear frequently in other topics. It is calculated
--   using the TF-IDF algorithm above. The stems generated by that
--   algorithm are them mapped back onto real words using the result of the
--   call to the topic_words function.
--
--  ARGUMENTS
--
--    topic_id    The identifier of the topic.
--    topic_text  The body of the topic (passed in for speed).
--
-- RETURNS
--
--   A table of five word-stem-tf_idf 3-tuples. The rows are sorted from
--   highest TF-IDF value (most characterising word) to lowest.
CREATE OR REPLACE FUNCTION topic_keywords (topic_id TEXT, topic_text TEXT)
  RETURNS TABLE(word TEXT, stem TEXT, tf_idf REAL) AS $$
    BEGIN
      RETURN QUERY SELECT tw.word, tw.stem, tfidf.tf_idf
                     FROM topic_tf_idf(topic_id) AS tfidf,
                          topic_words(topic_text) AS tw
                     WHERE tfidf.stem = tw.stem
                     ORDER BY tfidf.tf_idf DESC;
    END;
  $$ LANGUAGE plpgsql;


CREATE TABLE topic_keywords (
    topic_id  TEXT    PRIMARY KEY REFERENCES topic ON DELETE CASCADE,
    keywords  TEXT[]  DEFAULT NULL
);


CREATE OR REPLACE FUNCTION topic_keywords_update ()
  RETURNS TRIGGER AS $$
    DECLARE
      topic_text TEXT;
      new_keywords TEXT[];
    BEGIN
      topic_text := topic_body(NEW.topic_id);
      SELECT ARRAY(SELECT word FROM topic_keywords(NEW.topic_id, topic_text))
        INTO new_keywords;

      IF (TG_OP = 'UPDATE') THEN
        UPDATE topic_keywords SET keywords = new_keywords
          WHERE topic_id = NEW.topic_id;
      ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO topic_keywords VALUES(NEW.topic_id, new_keywords);
      END IF;

      RETURN NULL; -- The NULL is ignored, as this function is an after-trigger
    END;
$$ LANGUAGE 'plpgsql';
CREATE TRIGGER topic_update_trigger_02
  AFTER INSERT OR UPDATE ON topic
  FOR EACH ROW EXECUTE PROCEDURE topic_keywords_update ();


-- Installs up to and including GS 12.05 will need to populate the
-- full-text retrieval column, and hte keyword column of the topic table.
-- CREATE OR REPLACE FUNCTION topic_keywords_populate ()
--   RETURNS void AS $$
--     DECLARE
--       total_topics REAL;
--       trecord RECORD;
--       topic_text TEXT;
--       new_keywords TEXT[];
--       i REAL DEFAULT 0;
--       p REAL;
--     BEGIN
--       SELECT CAST(total_rows AS REAL) INTO total_topics
--         FROM rowcount WHERE table_name = 'topic';
--       FOR trecord IN SELECT * FROM topic WHERE keywords IS NULL LOOP
--         RAISE NOTICE 'Topic %', trecord.topic_id;
--         topic_text = topic_body(trecord.topic_id);
--         SELECT ARRAY(SELECT word
--                        FROM topic_keywords(trecord.topic_id, topic_text))
--           INTO new_keywords;
--         UPDATE topic SET keywords = new_keywords
--           WHERE topic.topic_id = trecord.topic_id;
--         i := i + 1;
--         p := (i / total_topics) * 100;
--         RAISE NOTICE '  Progress % %%', p;
--       END LOOP;
--     END;
-- $$ LANGUAGE 'plpgsql';
