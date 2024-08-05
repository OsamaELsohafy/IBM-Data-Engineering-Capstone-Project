#!/bin/bash

# Database credentials
DB_USER="root"
DB_PASS="MzAwLWVsc29oZmlv"
DB_NAME="sales"

# Export data
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME sales_data > sales_data.sql


