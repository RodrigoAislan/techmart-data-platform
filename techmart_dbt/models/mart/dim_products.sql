WITH products AS (
    SELECT *
    FROM {{ ref('stg_products') }}
)

SELECT
    PRODUCT_ID,
    TITLE AS PRODUCT_NAME,
    CATEGORY,
    BRAND
FROM products