query = """
SELECT
    o.order_id,
    o.order_date,
    o.order_year,
    o.order_month,
    c.customer_id,
    c.customer_name,
    c.segment,
    p.product_id,
    p.product_name,
    cat.category_name,
    sc.sub_category_name,
    g.country,
    g.state,
    g.city,
    r.region_name,
    oi.sales
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
JOIN sub_categories sc
    ON p.sub_category_id = sc.sub_category_id
JOIN categories cat
    ON sc.category_id = cat.category_id
JOIN geography g
    ON o.geo_id = g.geo_id
JOIN regions r
    ON g.region_id = r.region_id
"""
