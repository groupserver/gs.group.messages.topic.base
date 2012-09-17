SET CLIENT_ENCODING = 'UTF8';
SET CHECK_FUNCTION_BODIES = FALSE;
SET CLIENT_MIN_MESSAGES = WARNING;

-- The TF * IDF algorithm, in PL/pgSQL.
--
-- IDF (inverse document frequency) =
--          Total number of topics
--   _________________________________________
--    Count of the topics containing the term
--
-- The TF-IDF value for a word = TF * log(IDF). The code below calculates
--   the five top TF-IDF values for a newly updated topic.
CREATE OR REPLACE FUNCTION update_topic_keywords ()
  RETURNS TRIGGER
  AS $$
    DECLARE
      total_number_of_topics integer;
    BEGIN
      SELECT total_rows INTO total_number_of_topics 
        FROM rowcount WHERE table_name = 'topic';
      RETURN NULL;
    END;  
  $$ LANGUAGE plpgsql;
CREATE TRIGGER update_topic_keywords_trigger 
  AFTER INSERT OR UPDATE ON post -- Yes, AFTER; yes, post.
  EXECUTE PROCEDURE update_topic_keywords ();


-- TF (term frequency) = 
--               Count of the word in the topic
--   _________________________________________________________
--    Count of the most frequently occuring word in the topic
CREATE OR REPLACE FUNCTION topic_tf (topic_id TEXT)
  RETURNS TABLE (word TEXT, tf REAL) AS $$
    DECLARE
      ts_stat_inner TEXT;
      most_frequent_word_count REAL;
    BEGIN
      ts_stat_inner := 'SELECT fts_vectors FROM topic WHERE topic_id = ''' || topic_id || '''';
      SELECT CAST(ts.nentry AS REAL) INTO most_frequent_word_count 
        FROM ts_stat(ts_stat_inner) as ts
        ORDER BY nentry DESC LIMIT 1;
      RETURN QUERY SELECT cw.word, 
                     CAST(cw.nentry  / most_frequent_word_count AS REAL) AS tf
        FROM (SELECT ts.word, ts.nentry FROM ts_stat(ts_stat_inner) AS ts
                ORDER BY nentry DESC LIMIT 16) as cw; -- Power of 2;
    END;
  $$ LANGUAGE plpgsql;
-- select topic_tf('4GzdcBvbj8f70QexVQHUo3');

-- TF-IDF: Term Frequency --- Inverse Document Frequency
-- TF_IDF = TF * IDF
-- IDF = log(total topic count / number of topics containing the word)
CREATE OR REPLACE FUNCTION topic_tf_idf (topic_id TEXT)
  RETURNS TABLE (word TEXT, tf_idf REAL) AS $$
    DECLARE
      total_topics REAL;
    BEGIN
      SELECT CAST(total_rows AS REAL) INTO total_topics 
        FROM rowcount WHERE table_name = 'topic';
      RETURN QUERY 
        SELECT ttf.word, 
               CAST(ttf.tf * 
                    LOG(total_topics / 
                        (SELECT COUNT(*) FROM topic 
                           WHERE fts_vectors @@ CAST(ttf.word AS tsquery)))
                    AS REAL)
                  AS tf_idf
        FROM topic_tf(topic_id) as ttf
        ORDER BY tf_idf DESC
        LIMIT 5;
    END;
  $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION generate_topic_keywords (topic_id TEXT, 
                                                    topic_text TEXT,
                                                    topic_tsv tsvector)
  RETURNS TEXT AS $$
    DECLARE 
      r RECORD;
      v TABLE(word TEXT, pos TEXT);
    BEGIN
      select * into v from regexp_split_to_table(tsvector, E'\S');
      FOR r IN SELECT * FROM topic_tf_idf(topic_id) LOOP
        RAISE NOTICE 'Word %s', r.word;
        
      END LOOP;
      RETURN 'foo';
    END;
  $$ LANGUAGE plpgsql;


-- Get the first vector-offset for a stem
--
-- Description
--   The texts search vectors, used by the full-text retrieval system, is a
--   large list of "'stem':offset0,offset1,offset2". This function looks up
--   the vector for the stem, and returns the first offset.
--
-- Arguments
--   tsvs: The Text Search Vectors to search.
--   stem: The stem to look up in the text search vectors.
--
-- Returns
--   The value of the first offset for the stem.
CREATE OR REPLACE FUNCTION get_tsv_offset_for_stem (tsvs tsvector, stem TEXT)
  RETURNS INT as $$
    DECLARE
      stem_exp TEXT;
      ret TEXT[];
    BEGIN
      -- Yes, we are using regular expressions.
      stem_exp :=  E'.*''' || stem || E''':(\\d+?)[, $].*';
      -- Yes, we are turning the text search vector into a string.
      SELECT regexp_matches(CAST(tsvs AS TEXT), stem_exp) INTO ret;
      -- No, this is not the work of the just or the good.
      RETURN ret[1];
    END;
  $$ LANGUAGE plpgsql;
