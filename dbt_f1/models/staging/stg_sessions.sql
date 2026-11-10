with source as (
    select * from {{ source('raw_f1', 'sessions') }}
)

select
    (payload->>'session_key')::int as session_id,
    (payload->>'meeting_key')::int as meeting_id,
    payload->>'session_name' as session_name,
    payload->>'session_type' as session_type,
    (payload->>'date_start')::timestamptz as date_start,
    (payload->>'date_end')::timestamptz as date_end,
    (payload->>'year')::int as season_year,
    ingested_at
from source