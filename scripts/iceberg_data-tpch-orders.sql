USE iceberg_data.i_tpch;

CREATE TABLE orders (
   "orderkey" bigint NOT NULL,
   "custkey" bigint NOT NULL,
   "orderstatus" varchar(1) NOT NULL,
   "totalprice" double NOT NULL,
   "orderdate" date NOT NULL,
   "orderpriority" varchar(15) NOT NULL,
   "clerk" varchar(15) NOT NULL,
   "shippriority" integer NOT NULL,
   "comment" varchar(79) NOT NULL
);
