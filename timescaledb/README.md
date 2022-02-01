# [TimescaleDB](https://www.timescale.com)
## Requirements
- JDK 17
	- [PostgreSQL JDBC](https://jdbc.postgresql.org)
- Python 3
	- [psycopg2](https://www.psycopg.org)
```
pip install psycopg2-binary
```

	- [pandas](https://pandas.pydata.org)
```
pip install pandas
```

## Install TimescaleDB via Docker
1. Get the latest image of TimescaleDB
```
docker pull timescale/timescaledb:latest-pg14
```

2. Spin a container instance with telemetry turned off
```
docker run -d --name timescaledb -p 5432:5432 --env POSTGRES_PASSWORD=root --env TIMESCALEDB_TELEMETRY=off timescale/timescaledb:latest-pg14
```

## Set the Database

1. Connect to PostgreSQL instance (use `root` when prompted for password)
```
psql -U postgres -h localhost
```

2. Create a database called `metrics`
```
CREATE database metrics;
```

3. Connect to `metrics`
```
\c metrics
```

4. Add the TimescaleDB extension
```
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

## Run the Code
### Java
- Go to `java` code directory
```
cd timescaledb/java/io/github/iskandergaba/java
```

The PostgreSQL connector is bundled with the program so no need to worry about extra `classpath` configurations.

- **TSDBCreator.java:** Run this program to create a little database schema that simulates taking metrics over the last week.
```
java -cp *.jar TSDBCreator.java
```

- **TSDBDropper.java:** Run this program to drop the tables and all the data in `metrics` database.
```
java -cp *.jar TSDBDropper.java
```

### Python
- **TSDBReader.py:** Run this script to query the database into Pandas dataframes and print them.
```
python TSDBReader.py 
```

[Return to parent](../README.md)