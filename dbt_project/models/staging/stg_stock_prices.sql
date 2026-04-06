with source as (
    select * from read_parquet('../data/raw/stock_prices.parquet')
)

select
    Date as price_date,
    ticker,
    Open as open_price,
    High as high_price,
    Low as low_price,
    Close as close_price,
    Volume as trading_volume
from source
