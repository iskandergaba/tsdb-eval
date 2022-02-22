# [TimescaleDB](https://www.timescale.com) Demos
These demos assume the user is on Ubuntu (or a Debian Linux distribution at least)

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

## Sample Database Demo
In this demo, we create a `metrics` database that stores simulated system load for the last year along with different aggregations and data retention policies in Java, and read this database in Python.

### Set the Database

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

### Running the Code
#### Java
- Go to `java` code directory from the root
```bash
cd timescaledb/java/io/github/iskandergaba/db_demo/java
```

The PostgreSQL connector is bundled with the program so no need to worry about extra `classpath` configurations.

- **TSDBCreator.java:** Run this program to create a little database schema that simulates taking metrics over the last year.
```bash
java -cp ../../../../../../../lib/java/*.jar TSDBCreator.java

```

- **TSDBDropper.java:** Run this program to drop the tables and all the data in `metrics` database.
```bash
java -cp ../../../../../../../lib/java/*.jar TSDBDropper.java
```

#### Python
- Go to `python` code directory from the root
```bash
cd timescaledb/java/io/github/iskandergaba/db_demo/python
```
- **TSDBReader.py:** Run this script to query the database into Pandas dataframes and print them.
```bash
python TSDBReader.py 
```

## Monitoring Demo
In this demo, we create a `sys_load` database using a service where we store the system's CPU Load every 30 seconds. We then create continuous aggregation views of this information as follows:
- `cpu_load_24h`: Stores the last 24 hours of metrics on a 15 minutes frequency, update every 1 minute.
- `cpu_load_7d`: Stores the last week of metrics on an hourly frequency, updated every 5 minutes.
- `cpu_load_30d`: Stores the last 24 hours of metrics on a daily frequency, updated every 5 minutes.

One thing I wanted to achieve in this implementation is having **static** aggregation points of the previous **complete** time buckets while the current incomplete one remains dynamic and being updated. If we take `cpu_load_30d` as an example, we would have static aggregation values for the previous days, and a dynamic aggregation value for the current day, updated with the new data every 5 minutes.

### Running the code
- Go to `python` code directory from the root
```bash
cd timescaledb/java/io/github/iskandergaba/monitoring_demo/python
```
- Run `TSDBDemo.py` service to create the database and insert `cpu_load` data every 30 seconds. You can run it in the background using the following command:
```bash
python TSDBDemo.py &
```
- - Run `TSDBPlotter.py` service to plot the data from `cpu_load_24h`, `cpu_load_7d`, `cpu_load_30d` every one minute. The service only keeps the last 5 plots from eaach view. You can run it in the background using the following command:
```bash
python TSDBPlotter.py &
```

### Lessons Learnt from this demo
- While attempting to minimize the length of the data considered every aggregation, I stumbled upon this error message:
```
DETAIL:  The start and end offsets must cover at least two buckets in the valid time range of type "timestamp with time zone"
```
This meant that the closest start offset I could set for continuous aggregation policies was a little over two time buckets for it to work. So in general, I would advise the aggregation policy be of the following shape:
```SQL
SELECT add_continuous_aggregate_policy('view',
                    start_offset => INTERVAL '<2_TIMES_AGGREGATION_BUCKET_LENGTH>' + INTERVAL '<END_OFFSET>',
                    end_offset => INTERVAL '<END_OFFSET>',
                    schedule_interval => INTERVAL '<UPDATE_INTERVAL>');
```
- One potential runtime improvement I tried to implement was to define continuous aggregation views on other continuous aggregation views to spead up some low frequency aggregation operations instead of conducting all of them from scratch. For instance, instead of defining all continuous aggregation views on the main table `cpu_load`, I wanted to define `cpu_load_7d` on `cpu_load_24h` and `cpu_load_30` on `cpu_load_7d` to speed up the process for them. Unfortunately, this capability is not supported as of now. Fortunately, there seems to be a substantial community interest in the feature and an [open issue](https://github.com/timescale/timescaledb/issues/1400) is under serious consideration on TimescaleDB GitHub repository.


[Return to parent](../README.md)