
WITH customers AS (
    SELECT *
    FROM {{ ref('stg_customers') }}
)

SELECT
    CUSTOMER_ID,
    FIRST_NAME,
    LAST_NAME,
    EMAIL,
    COUNTRY,
    STATE,
    CITY
FROM customers
