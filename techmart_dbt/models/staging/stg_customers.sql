WITH source AS (

    SELECT
        PAYLOAD
    FROM TECHMART_DB.RAW.RAW_CUSTOMER_PAYLOADS

),

customers AS (

    SELECT
        customer.value AS customer_json
    FROM source,
        LATERAL FLATTEN(
            INPUT => source.PAYLOAD:users
        ) AS customer

)

SELECT
    customer_json:id::NUMBER AS customer_id,
    customer_json:firstName::VARCHAR AS first_name,
    customer_json:lastName::VARCHAR AS last_name,
    customer_json:age::NUMBER AS age,
    customer_json:gender::VARCHAR AS gender,
    customer_json:email::VARCHAR AS email,
    customer_json:phone::VARCHAR AS phone,
    customer_json:username::VARCHAR AS username,
    customer_json:address.city::VARCHAR AS city,
    customer_json:address.state::VARCHAR AS state,
    customer_json:address.country::VARCHAR AS country
FROM customers