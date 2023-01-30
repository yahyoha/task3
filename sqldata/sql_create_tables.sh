#!/bin/bash

#Table: allbilling
#Provider:String
#ProductName:String
#Date:Date
#Costs:Decimal
#UnitPrice:Decimal
#Quantity:Decimal
#CostResourceId:String
#CostResourceTag:Array[String]


#Table: allbilling_tags


docker exec -it docker_sql1_1 /opt/mssql-tools/bin/sqlcmd \
-S localhost -U SA -P "chiiKu4x*1" -Q "CREATE DATABASE cloudbillingtool;"

docker exec -it docker_sql1_1 /opt/mssql-tools/bin/sqlcmd \
-S localhost -U SA -P 'chiiKu4x*1' -Q \
"USE cloudbillingtool;CREATE TABLE allbilling (Provider NVARCHAR(255), ProductName NVARCHAR(255), Date DATE, Costs DECIMAL(18,2), UnitPrice DECIMAL(18,2), Quantity DECIMAL(18,2), CostResourceId NVARCHAR(255), CostResourceTag NVARCHAR(MAX));"

docker exec -it docker_sql1_1 /opt/mssql-tools/bin/sqlcmd \
-S localhost -U SA -P 'chiiKu4x*1' -Q \
"USE cloudbillingtool;CREATE TABLE allbilling_tags (Tag NVARCHAR(255));"

docker exec -it docker_sql1_1 /opt/mssql-tools/bin/sqlcmd \
-S localhost -U SA -P 'chiiKu4x*1' -Q \
"USE cloudbillingtool;SELECT * FROM allbilling;"
