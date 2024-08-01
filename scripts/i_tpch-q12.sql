SELECT
    l.shipmode,
    sum(case
        when o.orderpriority = '1-URGENT'
            OR o.orderpriority = '2-HIGH'
            then 1
        else 0
    end) as high_line_count,
    sum(case
        when o.orderpriority <> '1-URGENT'
            AND o.orderpriority <> '2-HIGH'
            then 1
        else 0
    end) AS low_line_count
FROM
    iceberg_data.i_tpch.orders o,
    iceberg_data.i_tpch.lineitem l
WHERE
    o.orderkey = l.orderkey
    AND l.shipmode in ('MAIL', 'SHIP')
    AND l.commitdate < l.receiptdate
    AND l.shipdate < l.commitdate
    AND l.receiptdate >= date '1994-01-01'
    AND l.receiptdate < date '1994-01-01' + interval '1' year
GROUP BY
    l.shipmode
ORDER BY
    l.shipmode;
