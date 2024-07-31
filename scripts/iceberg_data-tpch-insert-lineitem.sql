USE iceberg_data.i_tpch;

INSERT INTO lineitem
SELECT
  *
FROM
  "tpch"."sf1"."lineitem"
;
