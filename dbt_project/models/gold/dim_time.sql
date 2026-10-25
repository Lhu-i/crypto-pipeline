select distinct
    fetched_minute as minute_ts,
    (fetched_minute at time zone 'UTC')::date as date_day,
    extract(hour from (fetched_minute at time zone 'UTC'))::int as hour_utc,
    to_char(fetched_minute at time zone 'UTC', 'Dy') as day_name
from {{ ref('stg_prices') }}