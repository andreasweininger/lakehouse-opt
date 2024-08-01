USE hive_data.h_tpch;

INSERT INTO orders
SELECT
  *
FROM
  "tpch"."sf1"."orders"
;
