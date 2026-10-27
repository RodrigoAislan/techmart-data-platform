
WITH orders AS (

    SELECT *
    FROM {{ ref('stg_orders') }}

),

customers AS (

    SELECT *
    FROM {{ ref('stg_customers') }}

),

order_item_aggregates AS (

    SELECT
        ORDER_ID,
        COUNT(*) AS ITEM_LINE_COUNT,
        SUM(QUANTITY) AS ITEM_QUANTITY,
        SUM(LINE_TOTAL) AS ITEMS_GROSS_TOTAL,
        SUM(DISCOUNTED_TOTAL) AS ITEMS_DISCOUNTED_TOTAL

    FROM {{ ref('stg_order_items') }}
    GROUP BY ORDER_ID

)

SELECT
    -- Order identifiers
    o.ORDER_ID,
    o.CUSTOMER_ID,

    -- Customer attributes
    c.FIRST_NAME,
    c.LAST_NAME,
    c.EMAIL,
    c.COUNTRY,
    c.STATE,
    c.CITY,

    -- Order-level metrics from the source
    o.TOTAL AS ORDER_TOTAL,
    o.DISCOUNTED_TOTAL AS ORDER_DISCOUNTED_TOTAL,
    o.TOTAL_PRODUCTS,
    o.TOTAL_QUANTITY,

    -- Metrics aggregated from order items
    COALESCE(ia.ITEM_LINE_COUNT, 0) AS ITEM_LINE_COUNT,
    COALESCE(ia.ITEM_QUANTITY, 0) AS ITEM_QUANTITY,
    COALESCE(ia.ITEMS_GROSS_TOTAL, 0) AS ITEMS_GROSS_TOTAL,
    COALESCE(ia.ITEMS_DISCOUNTED_TOTAL, 0)
        AS ITEMS_DISCOUNTED_TOTAL,

    -- Reconciliation checks
    o.TOTAL - COALESCE(ia.ITEMS_GROSS_TOTAL, 0)
        AS GROSS_TOTAL_DIFFERENCE,

    o.DISCOUNTED_TOTAL
        - COALESCE(ia.ITEMS_DISCOUNTED_TOTAL, 0)
        AS DISCOUNTED_TOTAL_DIFFERENCE,

    -- Data lineage
    o.SOURCE_FILE AS ORDER_SOURCE_FILE

FROM orders AS o

INNER JOIN customers AS c
    ON o.CUSTOMER_ID = c.CUSTOMER_ID

LEFT JOIN order_item_aggregates AS ia
    ON o.ORDER_ID = ia.ORDER_ID
