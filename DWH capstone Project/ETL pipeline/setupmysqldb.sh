#!/bin/sh

# This startup script does the following
# Creates a database sales
# Uses the sales database
# Creates a table sales_data with fields rowid,productid,customerid,price,quantity and timestamp.


mysql --host=127.0.0.1 --port=3306 --user=root --password=<Replace with your mysqlserver password> -e "create database sales;
use sales;drop table if exists sales_data;create table sales_data(rowid int DEFAULT NULL,product_id int DEFAULT NULL,
customer_id int DEFAULT NULL,price decimal(10,0) DEFAULT NULL,
quantity int DEFAULT NULL,timestamp timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);"

# Loading data from sales_olddata.csv into sales_data table.This csv consists of data with old timestamp.

mysql --host=127.0.0.1 --port=3306 --user=root --password=<Replace with your mysqlserver password> -e "use sales;load data infile '/home/project/sales_olddata.csv' into table sales_data fields terminated BY ','lines terminated BY '\n';"

# Loading data from sales_newdata.csv into sales_data table.This csv consists of data updated with the current timestamp.
mysql --host=127.0.0.1 --port=3306 --user=root --password=<Replace with your mysqlserver password> -e "use sales;load data infile '/home/project/sales_newdata.csv' into table sales_data fields terminated BY ',' lines terminated BY '\n'(rowid,product_id,customer_id,price, quantity);"



