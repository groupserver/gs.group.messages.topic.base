SET CLIENT_ENCODING = 'UTF8';
SET CHECK_FUNCTION_BODIES = FALSE;
SET CLIENT_MIN_MESSAGES = WARNING;
--
-- Initialise trigger and rowcount for the topic table
--
BEGIN;
   -- Make sure no rows can be added to topic until we have finished
   LOCK TABLE topic IN SHARE ROW EXCLUSIVE MODE;

   CREATE TRIGGER count_topic_rows
      AFTER INSERT OR DELETE on topic
      FOR EACH ROW EXECUTE PROCEDURE count_rows();
   
   -- Initialise the row count record
   DELETE FROM rowcount WHERE table_name = 'topic';

   INSERT INTO rowcount (table_name, total_rows)
   VALUES  ('topic',  (SELECT COUNT(*) FROM topic));

COMMIT;
