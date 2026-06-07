-- name: list_activities_for_user
-- Recent activities for a user, newest first.
select id, source, external_id, sport, name, start_time, elapsed_time_s,
       distance_m, start_lat, start_lng, stream_object_key
  from activities
 where user_id = :user_id
 order by start_time desc
 limit :limit;


-- name: get_activity^
-- Single activity by id (^ = one row or None).
select id, user_id, source, external_id, sport, name, start_time, elapsed_time_s,
       distance_m, start_lat, start_lng, stream_object_key, summary, weather
  from activities
 where id = :id;
