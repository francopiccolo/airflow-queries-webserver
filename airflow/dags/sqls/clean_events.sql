INSERT INTO events
SELECT
        es.event,
        es.time,
        es.unique_visitor_id,
        es.ha_user_id,
        es.browser,
        es.os,
        COALESCE(c.code, es.country_code)
  FROM  events_stg es
  LEFT  JOIN countries c
    ON  es.country_code = c.name
  LEFT  JOIN events e
    ON  es.event = e.event
   AND  es.time = e.time
   AND  es.unique_visitor_id = e.unique_visitor_id
 WHERE  e.event IS NULL;