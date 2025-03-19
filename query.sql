SELECT 
    cp.product_id, 
    SUM(
        CASE 
            WHEN cp.quantity * pp.price < 50 THEN 0 
            ELSE cp.quantity * pp.price 
        END
    ) AS total, 
    cp.country
FROM customer_purchases cp
LEFT JOIN product_price pp 
    ON cp.product_id = pp.product_id
WHERE 
    cp.purchase_date >= pp.valid_from 
    AND (cp.purchase_date <= pp.valid_to OR pp.valid_to IS NULL)
    AND cp.customer_id IN (
        SELECT customer_id 
        FROM customer_purchases 
        GROUP BY customer_id 
        HAVING COUNT(*) >= 10
    )
GROUP BY cp.product_id, cp.country 
ORDER BY total DESC;