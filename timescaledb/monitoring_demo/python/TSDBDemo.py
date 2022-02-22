import time
import psutil
import psycopg2

DB_NAME = "sys_load"

def main():
    # Initialize the database
    connection = init_db("postgres", "root", "localhost", "5432", DB_NAME)
    set_policies(connection)
    while True:
        insert_data(connection, psutil.cpu_percent())
        time.sleep(5)

# Create the database
def init_db(user, password, host, port, dbname):
    connection = psycopg2.connect(user=user,
                                password=password,
                                host=host,
                                port=port)
    connection.autocommit = True
    cursor = connection.cursor()

    # Drop database if it exists
    sql = "DROP DATABASE IF EXISTS {}".format(dbname)
    cursor.execute(sql)

    # Create database if it exists
    sql = "CREATE DATABASE {}".format(dbname)
    cursor.execute(sql)

    cursor.close()
    connection.close()

    # Connect to the database
    connection = psycopg2.connect(user=user,
                                password=password,
                                host=host,
                                port=port,
                                database=dbname)
    connection.autocommit = True
    cursor = connection.cursor()

    # Create `cpu_load` table
    sql = """CREATE TABLE cpu_load(
            ts TIMESTAMPTZ NOT NULL,
            load DOUBLE PRECISION);"""
    cursor.execute(sql)

    sql = "SELECT create_hypertable('cpu_load', 'ts');"
    cursor.execute(sql)

    # Create continuous aggregation materialized views
    sql = """CREATE MATERIALIZED VIEW cpu_load_24h
                    WITH (timescaledb.continuous) AS
                    SELECT time_bucket(INTERVAL '15 minutes', ts) AS ts_bucket,
                       MIN(load) AS min_load,
                       AVG(load) AS avg_load,
                       MAX(load) AS max_load
                    FROM cpu_load
                    GROUP BY ts_bucket;"""
    cursor.execute(sql)

    sql = """CREATE MATERIALIZED VIEW cpu_load_7d
                    WITH (timescaledb.continuous) AS
                    SELECT time_bucket(INTERVAL '1 hour', ts) AS ts_bucket,
                       MIN(load) AS min_load,
                       AVG(load) AS avg_load,
                       MAX(load) AS max_load
                    FROM cpu_load
                    GROUP BY ts_bucket;"""
    cursor.execute(sql)

    sql = """CREATE MATERIALIZED VIEW cpu_load_30d
                    WITH (timescaledb.continuous) AS
                    SELECT time_bucket(INTERVAL '24 hours', ts) AS ts_bucket,
                       MIN(load) AS min_load,
                       AVG(load) AS avg_load,
                       MAX(load) AS max_load
                    FROM cpu_load
                    GROUP BY ts_bucket"""
    cursor.execute(sql)

    cursor.close()
    return connection

# Set policies
def set_policies(connection):
    cursor = connection.cursor()

    # Set continuous aggregation policies for views
    ## Set a continuous aggregation on the `cpu_load_24h` view
    sql = """SELECT add_continuous_aggregate_policy('cpu_load_24h',
                    start_offset => INTERVAL '30 minutes' + INTERVAL '1 minute',
                    end_offset => INTERVAL '1 minute',
                    schedule_interval => INTERVAL '1 minute');"""
    cursor.execute(sql)

    ## Set a continuous aggregation on the `cpu_load_7d` view
    sql = """SELECT add_continuous_aggregate_policy('cpu_load_7d',
                    start_offset => INTERVAL '2 hours' + INTERVAL '5 minutes',
                    end_offset => INTERVAL '5 minutes',
                    schedule_interval => INTERVAL '5 minutes');"""
    cursor.execute(sql)

    ## Set a continuous aggregation on the `cpu_load_30d` view
    sql = """SELECT add_continuous_aggregate_policy('cpu_load_30d',
                    start_offset => INTERVAL '48 hours' + INTERVAL '5 minutes',
                    end_offset => INTERVAL '5 minutes',
                    schedule_interval => INTERVAL '5 minutes');"""
    cursor.execute(sql)

    # Set a retention policy of 48 hours and 10 minutes on the `cpu_load` table
    sql = "SELECT add_retention_policy('cpu_load', INTERVAL '48 hours' + INTERVAL '10 minutes')"
    cursor.execute(sql)

    # Set retention policies on views2
    ## Set a retention policy of 24 hours on the `cpu_load_24h` view
    sql = "SELECT add_retention_policy('cpu_load_24h', INTERVAL '24 hours')"
    cursor.execute(sql)

    ## Set a retention policy of 7 days on the `cpu_load_7d` view
    sql = "SELECT add_retention_policy('cpu_load_7d', INTERVAL '7 days')"
    cursor.execute(sql)

    ## Set a retention policy of 30 days on the `cpu_load_30d` view
    sql = "SELECT add_retention_policy('cpu_load_30d', INTERVAL '30 days')"
    cursor.execute(sql)

    cursor.close()

# Insert CPU load data point
def insert_data(connection, cpu_load):
    cursor = connection.cursor()
    sql = """INSERT INTO cpu_load VALUES (now(), {})""".format(cpu_load)
    cursor.execute(sql)

    cursor.close()

if __name__ == "__main__":
    main()