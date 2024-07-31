USE iceberg_data.i_tpch;

CREATE TABLE lineitem (
   "orderkey" bigint NOT NULL,
   "partkey" bigint NOT NULL,
   "suppkey" bigint NOT NULL,
   "linenumber" integer NOT NULL,
   "quantity" double NOT NULL,
   "extendedprice" double NOT NULL,
   "discount" double NOT NULL,
   "tax" double NOT NULL,
   "returnflag" varchar(1) NOT NULL,
   "linestatus" varchar(1) NOT NULL,
   "shipdate" date NOT NULL,
   "commitdate" date NOT NULL,
   "receiptdate" date NOT NULL,
   "shipinstruct" varchar(25) NOT NULL,
   "shipmode" varchar(10) NOT NULL,
   "comment" varchar(44) NOT NULL
);
