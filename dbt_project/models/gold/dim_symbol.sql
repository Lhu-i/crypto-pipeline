select
    md5(symbol) as symbol_key,
    symbol,
    replace(symbol, 'USDT', '') as base_asset,
    'USDT' as quote_asset
from (
    select distinct symbol
    from {{ ref('stg_prices') }}
) s