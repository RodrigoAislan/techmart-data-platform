
WITH order_items AS (

    SELECT *
    FROM {{ ref('int_order_items_enriched') }}

)

SELECT
    -- Business keys
    ORDER_ID,
    CUSTOMER_ID,
    PRODUCT_ID,

    -- Customer dimensions
    COUNTRY,
    STATE,
    CITY,

    -- Product dimensions
    PRODUCT_TITLE,
    PRODUCT_CATEGORY,
    PRODUCT_BRAND,

    -- Sales measures
    QUANTITY,
    UNIT_PRICE,
    LINE_TOTAL AS GROSS_SALES_AMOUNT,
    ITEM_DISCOUNT_PERCENTAGE,
    ITEM_DISCOUNTED_TOTAL AS NET_SALES_AMOUNT,

    -- Order context
    ORDER_TOTAL,
    ORDER_DISCOUNTED_TOTAL,
    ORDER_TOTAL_PRODUCTS,
    ORDER_TOTAL_QUANTITY,

    -- Data lineage
    ORDER_ITEM_SOURCE_FILE

FROM order_items
