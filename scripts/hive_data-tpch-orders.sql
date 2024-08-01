USE hive_data.h_tpch;

CREATE TABLE orders (
   "orderkey" bigint,
   "custkey" bigint,
   "orderstatus" varchar(1),
   "totalprice" double,
   "orderdate" date,
   "orderpriority" varchar(15),
   "clerk" varchar(15),
   "shippriority" integer,
   "comment" varchar(79)
);
