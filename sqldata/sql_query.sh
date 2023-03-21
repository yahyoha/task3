#!/bin/bash

echo "Query data for table allbilling"
docker exec -it docker_sql1_1 /opt/mssql-tools/bin/sqlcmd \
-S localhost -U SA -P 'chiiKu4x*1' -Q \
"USE cloudbillingtool;SELECT TOP(10) * FROM allbilling;"

echo "Query data for table allbilling_tags"
docker exec -it docker_sql1_1 /opt/mssql-tools/bin/sqlcmd \
-S localhost -U SA -P 'chiiKu4x*1' -Q \
"USE cloudbillingtool;SELECT Tag FROM allbilling_tags;"
