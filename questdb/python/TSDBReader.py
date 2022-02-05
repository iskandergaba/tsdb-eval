import psycopg2
import pandas as pd

CONNECTION = "postgres://admin:quest@localhost:8812/qdb"

def main():  
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()


    # Drop data older than one month
    print('\nManual data retention: Dropping data older than one month...')
    query = """ALTER TABLE sys_load DROP PARTITION
                WHERE time < dateadd('d', -30, now())"""
    cursor.execute(query)
    print('\nDone.')


    # Get the first 10 data results
    print('\nsys_load')
    query = """SELECT *
                FROM sys_load
                ORDER BY time ASC
                LIMIT 10"""
    cursor.execute(query)
    results = cursor.fetchall()
    sys_load_df = pd.DataFrame(results, columns=['time', 'cpu_load', 'memory_usage', 'network_usage'])
    sys_load_df.set_index('time', inplace=True)
    print(sys_load_df)

    # Get the first 24 hours of aggregations
    print('\nsys_load_hourly')
    query = """SELECT *
                FROM sys_load_hourly
                ORDER BY time ASC
                LIMIT 24"""
    cursor.execute(query)
    results = cursor.fetchall()
    sys_load_hourly_df = pd.DataFrame(results, columns=['time', 'cpu_load', 'memory_usage', 'network_usage'])
    sys_load_hourly_df.set_index('time', inplace=True)
    print(sys_load_hourly_df)

    cursor.close()

if __name__ == "__main__":
    main()