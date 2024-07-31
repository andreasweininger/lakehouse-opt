USE hive_data.h_tpch;

SELECT
    sum(extendedprice * discount) as revenue
FROM
    lineitem
WHERE
    shipdate >= date '1994-01-01'
    AND shipdate < date '1994-01-01' + interval '1' year
    AND discount between 0.06 - 0.01 AND 0.06 + 0.01
    AND quantity < 24;
