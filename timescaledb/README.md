# [TimescaleDB](https://www.timescale.com)
This demo assumes the user is on Ubuntu (or a Debian Linux distribution at least)

## Requirements
- Docker
	- [Ubuntu Installation Guide](https://docs.docker.com/engine/install/ubuntu)
	- [Debian Installation Guide](https://docs.docker.com/engine/install/debian)
- JDK 17
	- [PostgreSQL JDBC](https://jdbc.postgresql.org)
- Python 3
	- [psycopg2](https://www.psycopg.org)
	- [pandas](https://pandas.pydata.org)

```bash
pip install psycopg2-binary pandas
```

- PostgreSQL
```bash
sudo apt-get install wget ca-certificates

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

sudo apt update

sudo apt -y install postgresql-14
```

## Install TimescaleDB
1. Get the latest image of TimescaleDB
```bash
docker pull timescale/timescaledb:latest-pg14
```

2. Spin a container instance with telemetry turned off
```bash
docker run -d --name timescaledb -p 5432:5432 --env POSTGRES_PASSWORD=root --env TIMESCALEDB_TELEMETRY=off timescale/timescaledb:latest-pg14
```

## Set the Database

1. Connect to PostgreSQL instance (use `root` when prompted for password)
```bash
psql -U postgres -h localhost
```

2. Create a database called `metrics`
```sql
CREATE database metrics;
```

3. Connect to `metrics`
```sql
\c metrics
```

4. Add the TimescaleDB extension
```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

## Run the Code
### Java
- Go to `java` code directory
```bash
cd timescaledb/java/io/github/iskandergaba/java
```

The PostgreSQL connector is bundled with the program so no need to worry about extra `classpath` configurations.

- **TSDBCreator.java:** Run this program to create a little database schema that simulates taking metrics over the last week.
```bash
java -cp *.jar TSDBCreator.java
```

- **TSDBDropper.java:** Run this program to drop the tables and all the data in `metrics` database.
```bash
java -cp *.jar TSDBDropper.java
```

### Python
- **TSDBReader.py:** Run this script to query the database into Pandas dataframes and print them.
```bash
python TSDBReader.py 
```

[Return to parent](../README.md)