select
    md5(symbol || '|' || fetched_minute::text) as price_key,
    md5(symbol) as symbol_key,
    fetched_minute as minute_ts,
    samples,
    avg_price,
    min_price,
    max_price
from {{ ref('price_per_minute') }}