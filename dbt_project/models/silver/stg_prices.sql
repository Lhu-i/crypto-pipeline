select
    id,
    symbol,
    price,
    fetched_at,
    date_trunc('minute', fetched_at) as fetched_minute
from public.raw_prices
where price > 0
  and symbol is not null