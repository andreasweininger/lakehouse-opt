USE hive_data.h_tpch;

INSERT INTO lineitem
SELECT
  *
FROM
  "tpch"."sf1"."lineitem"
;
