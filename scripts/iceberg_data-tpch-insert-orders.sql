USE iceberg_data.i_tpch;

INSERT INTO orders
SELECT
  *
FROM
  "tpch"."sf1"."orders"
;
