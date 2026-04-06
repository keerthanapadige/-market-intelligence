with staging as (
    -- This 'ref' function is dbt's secret weapon. 
    -- It tells dbt to look at our cleaned staging data first.
    select * from {{ ref('stg_stock_prices') }}
)

select
    price_date,
    ticker,
    close_price,
    -- Window Function: Get the price from the PREVIOUS day for the same ticker
    lag(close_price) over (partition by ticker order by price_date) as prev_close_price,
    -- Calculation: (%) Change
    ((close_price - prev_close_price) / prev_close_price) * 100 as daily_return_pct
from staging
