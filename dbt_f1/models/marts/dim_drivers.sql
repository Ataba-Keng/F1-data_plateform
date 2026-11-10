with stg_drivers as (
    select * from {{ ref('stg_drivers') }}
)

select
    driver_number,
    driver_code,
    full_name,
    team_name,
    team_color,
    country_code,
    ingested_at as dwh_updated_at
from stg_drivers