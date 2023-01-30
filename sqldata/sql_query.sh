#!/bin/bash

docker exec -it docker_sql1_1 /opt/mssql-tools/bin/sqlcmd \
-S localhost -U SA -P 'chiiKu4x*1' -Q \
"USE cloudbillingtool;SELECT COUNT(*) FROM allbilling;"
