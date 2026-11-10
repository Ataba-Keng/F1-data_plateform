with source as (
    select * from {{ source('raw_f1', 'drivers') }}
)

select
    (payload->>'driver_number')::int as driver_number,
    payload->>'broadcast_name' as broadcast_name,
    payload->>'full_name' as full_name,
    payload->>'name_acronym' as driver_code,
    payload->>'team_name' as team_name,
    payload->>'team_colour' as team_color,
    payload->>'country_code' as country_code,
    ingested_at
from source