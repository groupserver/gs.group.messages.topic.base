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
  $$  LANGUAGE plpgsql;
-- select topic_tf('4GzdcBvbj8f70QexVQHUo3');
