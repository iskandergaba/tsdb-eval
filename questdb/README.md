# [QuestDB](https://www.questdb.io)
## Requirements
- Docker
	- [Ubuntu Installation Guide](https://docs.docker.com/engine/install/ubuntu)
	- [Debian Installation Guide](https://docs.docker.com/engine/install/debian)
- JDK 17
	- [PostgreSQL JDBC](https://jdbc.postgresql.org)
- Python 3
	- [psycopg2](https://www.psycopg.org)
        - `pip install psycopg2-binary`
	- [pandas](https://pandas.pydata.org)
        - `pip install pandas`

- PostgreSQL (Optional)
```bash
sudo apt-get install wget ca-certificates

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

sudo apt update

sudo apt -y install postgresql-14
```

## Install QuestDB via Docker
1. Get the latest image of TimeScaleDB
```
docker pull questdb/questdb
```

2. Spin a container instance with telemetry turned off
```
docker run -d --name questdb \
 -e QDB_TELEMETRY_ENABLED=FALSE \
 -p 9000:9000 \
 -p 9009:9009 \
 -p 8812:8812 \
 -p 9003:9003 \
 questdb/questdb
```

## Set the Database

1. You can use `psql` to connect QuestDB using `localhost`, `8812` as a port, and `quest` as a password from terminal:
```bash
psql -U admin -h localhost -p 8812
```


## Run the Code
### Java
- Go to `java` code directory
```bash
cd timescaledb/java/io/github/iskandergaba/java
```

The PostgreSQL connector is bundled with the program so no need to worry about extra `classpath` configurations.

- **TSDBCreator.java:** Run this program to create a little database schema that simulates taking metrics over the last year.
```bash
java -cp ../../../../../../lib/java/*.jar TSDBCreator.java

```

- **TSDBDropper.java:** Run this program to drop the tables and all the data in `metrics` database.
```bash
java -cp ../../../../../../lib/java/*.jar TSDBDropper.java
```

### Python
- **TSDBReader.py:** Run this script to query the database into Pandas dataframes and print them.
```bash
python TSDBReader.py 
```

[Return to parent](../README.md)