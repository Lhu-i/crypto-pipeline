select
    symbol,
    fetched_minute,
    count(*) as samples,
    round(avg(price), 4) as avg_price,
    min(price) as min_price,
    max(price) as max_price
from {{ ref('stg_prices') }}
group by symbol, fetched_minute