with source as (
    select * from {{ source('raw_f1', 'meetings') }}
)

select
    (payload->>'meeting_key')::int as meeting_id,
    (payload->>'year')::int as season_year,
    payload->>'meeting_name' as meeting_name,
    payload->>'meeting_official_name' as official_name,
    payload->>'location' as location,
    payload->>'country_name' as country_name,
    (payload->>'circuit_key')::int as circuit_id,
    payload->>'circuit_short_name' as circuit_name,
    payload->>'circuit_type' as circuit_type,
    (payload->>'date_start')::timestamptz as date_start,
    (payload->>'date_end')::timestamptz as date_end,
    (payload->>'is_cancelled')::boolean as is_cancelled,
    ingested_at
from source